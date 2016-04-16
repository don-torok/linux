#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import pprint
import getopt
import smtplib
import json
from email.mime.text import MIMEText
from os.path import expanduser
from subprocess import call


#
# get s3 access keys from ~/.s3cfg
#

def usage():
    print( 'getUnload.py [--debug] --s3 <s3Bucket> --manifest <manifest prefix> \n' )
    print( 'use s3cmd to get the files listed in the manifest.  Concatenate into a single file named manifest prefix' )
    print( 'e.g. unload.py  --s3 /dtk-transfer/mslr_cdm4 --manifest drug_era' )
    print( '     will create a file drug_era.gz in the local directory \n' )

# read s3 access and secret keys from s3cfg file
def getS3keys():
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

    debug = False
    bucket   = ''
    manifest = ''

    try:
        opts, args = getopt.getopt( argv, "", ["debug", "s3=", "manifest="] )

    except getopt.GetoptError as err:
        print ( err )
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--debug":
            debug = True
        elif opt == "--s3":
            bucket = arg
            if bucket.rfind('/') != len( bucket ) - 1:
                bucket += '/'
        elif opt == "--manifest":
            manifest = arg    
        else:
            usage()
            sys.exit()

    if not bucket or not manifest:
        usage()
        sys.exit(2)

    s3Keys = getS3keys()
    
    command = 's3cmd get s3:/' + bucket + manifest + '_manifest'
    if debug:
        print command
    
    try:
        call( [ command ], shell=True )
    except:
        print( '"' + command + '" failed \n' ) 
        sys.exit(2)

    #  Read and parse manifest
    try:
        f = open( manifest + '_manifest', 'r' )
    except:
        print( 'failed to open manifest: ' + manifest + '_manifest \n' )
        sys.exit(2)

    parsed_manifest = json.load(f)

    # get file concatinate into manifest.gz
    first_file = True
    for urls in parsed_manifest[ 'entries' ]:
        command = 's3cmd get ' + urls[ 'url' ]
        if first_file:
            command +=  ' ' + manifest + '.gz'

        if debug:
            print( command )

        try:
            call( [ command ], shell=True )
        except:
            print( '"' + command + '" failed \n' ) 
            sys.exit(2)

        # if not first file cat into manifest.gz
        if first_file:
            first_file = False
        else:
            url_split = urls[ 'url' ].split('/')
            filename = url_split[ -1 ]
            command = 'cat ' + filename + ' >> ' + manifest + '.gz'
            if debug:
                print( command )
            
            try:
                call( [ command ], shell=True )
            except:
                print( '"' + command + '" failed \n' ) 
                sys.exit(2)

    msg = MIMEText( 'getUnload complete: for ' + manifest )
    msg['Subject'] = 'getUnload from S3'
    msg['From']    = 'torok@omop.org'
    msg['To']      = 'torok@omop.org'
    s = smtplib.SMTP('localhost')
    s.sendmail( 'torok@omop.org', ['torok@omop.org'], msg.as_string() )
    s.quit()


if __name__ == "__main__":
    main(sys.argv[1:])


