#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys

conn = None

try:
     
    conn = psycopg2.connect( database="ims"
                           , user="dtorok"
                           , password=""
                           , host="rs-ims.cra03mppdtga.us-east-1.redshift.amazonaws.com"
                           , port="5439"
                           ) 
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) 
    cur = conn.cursor()
    cur.execute('SELECT version()')          
    ver = cur.fetchone()
    print ver    
    

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if conn:
        conn.close()
