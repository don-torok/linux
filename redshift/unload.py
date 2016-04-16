#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import pprint
import getopt
import smtplib
from email.mime.text import MIMEText
from os.path import expanduser

#
# get s3 access keys from ~/.s3cfg
#

def usage():
    print( 'unload.py [--debug] --user <user> ' \
               + '--password <password> --table <tableName> --schema <schema> --s3 <s3Bucket> \n' )
    print( 'Will unload table to s3Bucket/schema/table' )
    print( 'e.g. unload.py --user dtorok --password xxyyzz --table drug_era --schema mslr_cdm4 --s3 /dtk-transfer/  ' )
    print( 'use getUnload.py to copy the results from S3 to local computer \n' )

# read s3 access and secret keys from s3cfg file
def getS3Keys():
    try:
        access_key = ''
        secret_key = ''

        fileName = expanduser('~') + '/.s3cfg'
        f = open( fileName, 'r' )
        for line in f.readlines():
            if line.find( 'access_key' ) == 0:
                access_key = line.split( '=' )[1]
            if line.find( 'secret_key' ) == 0:
                secret_key = line.split( '=' )[1]

        if not access_key or not secret_key:
            print( 'Cannot parse s3 config file' )
            sys.exit(2)

        return( access_key.strip(), secret_key.strip() )

    except:
        print( 'Cannot open s3 config file' + fileName )
        sys.exit(2)



def main( argv ):

    conn = None
    password = ''
    database = 'truven'
    user = ''
    password = ''
    table = ''
    schema = ''
    bucket = ''
    debug = False

    try:
        opts, args = getopt.getopt( argv, "", ["debug", "user=", "password=", "table=", "schema=", "s3=" ] )

    except getopt.GetoptError as err:
        print ( err )
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--debug":
            debug = True
        elif opt == "--password":
            password = arg
        elif opt == "--user":
            user = arg    
        elif opt == "--table":
            table = arg    
        elif opt == "--schema":
            schema = arg    
        elif opt == "--s3":
            bucket = arg    
        else:
            usage()
            sys.exit()

    if not user or not password or not table or not schema or not bucket:
        usage()
        sys.exit(2)


    try:
     
        conn = psycopg2.connect( database="truven"
                                 , user= user
                                 , password= password
                                 , host="omop-datasets.cqlmv7nlakap.us-east-1.redshift.amazonaws.com"
                                 , port="5439"
                                 ) 
    # with out autocommit, script runs, but no row in tablesq
        conn.autocommit = True
        cur = conn.cursor()


        UnloadFrom = 'SELECT * FROM ' + schema + '.' + table 
        UnloadTo   = 's3:/' + bucket + schema + '/' + table + '_'

        command = "unload ('%s') to '%s' " % ( UnloadFrom, UnloadTo )
        command += "CREDENTIALS " \
            + "'aws_access_key_id=%s;" \
            + "aws_secret_access_key=%s' " 
        command += "manifest gzip addQuotes allowOverWrite"

        if debug:
            # don't show access and secret key in print command
            print command % ('<access_key>', '<secret_key>' )

        # getS3 keys from config file
        command = command % getS3Keys()

        cur.execute( command )

        conn.commit

        msg = MIMEText( 'Unload complete:' + UnloadFrom + ' to ' + UnloadTo )
        msg['Subject'] = 'Unload RedShift to S3'
        msg['From']    = 'torok@omop.org'
        msg['To']      = 'torok@omop.org'
        s = smtplib.SMTP('localhost')
        s.sendmail( 'torok@omop.org', ['torok@omop.org'], msg.as_string() )
        s.quit()
    
    except psycopg2.DatabaseError, e:
        errorText = e.pgerror
        print '%s' % e.pgerror
        msg = MIMEText( 'Unload failed ' + errorText )
        msg['Subject'] = 'Unload RedShift to S3'
        msg['From']    = 'torok@omop.org'
        msg['To']      = 'torok@omop.org'
        s = smtplib.SMTP('localhost')
        s.sendmail( 'torok@omop.org', ['torok@omop.org'], msg.as_string() )
        s.quit()
        sys.exit(1)

    finally:
    
        if conn:
            conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])
