#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import pprint

conn = None

try:
     
    conn = psycopg2.connect( database="truven"
                           , user="dtorok"
                           , password="password"
                           , host="omop-datasets.cqlmv7nlakap.us-east-1.redshift.amazonaws.com"
                           , port="5439"
                           ) 
#    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) 
    cur = conn.cursor()
    cur.execute( 'select * from stl_load_errors' )
    records = cur.fetchall()
    pprint.pprint( records )    

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)
    
    
finally:
    
    if conn:
        conn.close()
