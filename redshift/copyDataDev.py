#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import pprint
import smtplib
from email.mime.text import MIMEText

conn = None

try:
     
    conn = psycopg2.connect( database="omopdev"
                           , user="dtorok"
                           , password="password"
                           , host="omop-rs-dev.cat5ur0p6375.us-east-1.redshift.amazonaws.com"
                           , port="5439"
                           ) 
    # with out autocommit, script runs, but no row in tablesq
    conn.autocommit = True
    cur = conn.cursor()

    copyFrom = 's3://dtk-transfer/vocabulary_4_5/drug_strength_manifest'
    copyTo   = 'vocabulary_4_5.drug_strength'

    command = "copy %s from '%s' " % ( copyTo, copyFrom )
    command += "CREDENTIALS " \
        + "'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
        + "aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY' " \
        + "manifest gzip removeQuotes"

    print command
    cur.execute( command )

    conn.commit

    msg = MIMEText( 'Copy committed' )
    msg['Subject'] = 'Copy S3 to Redshift'
    msg['From']    = 'torok@omop.org'
    msg['To']      = 'torok@omop.org'
    s = smtplib.SMTP('localhost')
    s.sendmail( 'torok@omop.org', ['torok@omop.org'], msg.as_string() )
    s.quit()
    
except psycopg2.DatabaseError, e:
    errorText = e.pgerror
    print '%s' % e.pgerror
    msg = MIMEText( 'Copy failed ' + errorText )
    msg['Subject'] = 'Copy S3 to Redshift'
    msg['From']    = 'torok@omop.org'
    msg['To']      = 'torok@omop.org'
    s = smtplib.SMTP('localhost')
    s.sendmail( 'torok@omop.org', ['torok@omop.org'], msg.as_string() )
    s.quit()
    sys.exit(1)

    
finally:
    
    if conn:
        conn.close()

