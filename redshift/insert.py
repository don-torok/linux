#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys


cars = (
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Citroen', 21000),
    (7, 'Hummer', 41400),
    (8, 'Volkswagen', 21600)
)

conn = None

try:
     
    conn = psycopg2.connect( database="truven"
                           , user="dtorok"
                           , password="password"
                           , host="omop-datasets.cqlmv7nlakap.us-east-1.redshift.amazonaws.com"
                           , port="5439"
                           ) 
  
    cur = conn.cursor()  
    
    try:
        cur.execute("DROP TABLE car")
    except:
        pass


    cur.execute("CREATE TABLE car(id INT PRIMARY KEY, name TEXT, price INT)")
    query = "INSERT INTO car (id, name, price) VALUES (%s, %s, %s)"
    cur.executemany(query, cars)
        
    conn.commit()
    

except psycopg2.DatabaseError, e:
    
    if conn:
        conn.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if conn:
        conn.close()
