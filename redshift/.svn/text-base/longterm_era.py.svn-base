#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# Humedica specific code to create longTerm era
#
# PreConditions:
#   1) Empty longTerm_era table ( ptId, start_date, end_date, first_enc )
#   2) Select access to schema.encounter
#
# PostConditon:
#   longTerm_era table filled in with ptId, start_date, end_date, first_enc
#   
#
# Run string
#   longTerm_era.py [--help] [--debug] --user <user> --password <password> --schema <schema>
#                 --targetSchema [<target schema if different from source>]
#
# 
# Logic
# First create a table of all unique longTerm encounters where the visitId is not defined.
# The next part of the programs is recursive.  A temporary table is created that joins
# IP encounters for the same person where the two exposures are on consecutive days
# The resultant table is then processed again join consecutive eras.  This continues until no
# new eras are created.
#
#
# Change Log
#  Who     When        What
#  DTk    15Jan2015  Copied logic from drug eras
#
import psycopg2
import psycopg2.extras
import sys
import datetime
import time
import getopt

def usage():
            print( 'longterm_era.py [--help] [--debug] --user <user> --password <password> --schema <schema>' \
                + ' --targetSchema [<target schema if different from source>]' \
                + ' --vocabSchema [<vocabulary schema if different from source>]' \
                 )
def executeSQL( cursor, statement, debug ):
    if debug:
        print( statement )
    cursor.execute( statement )


def main( argv ):
    
    schema   = ''
    targetSchema = ''
    user     = ''
    password = ''
    vocab_db = ''
    debug  = False
    inpatient =  'Inpatient'
    longTerm=  'Nursing home inpatient'
  
    try:
        opts, args = getopt.getopt( argv, "", ["help", "debug", "user=", "password="\
                                  , "schema=", "targetSchema=", "vocabSchema=" ] )

    except getopt.GetoptError as err:
        print ( err )
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--help":
            usage()
            sys.exit()
        elif opt == "--user":
            user = arg
        elif opt == "--password":
            password = arg
        elif opt == "--schema":
            schema = arg
        elif opt == "--targetSchema":
            targetSchema = arg
        elif opt == "--vocabSchema":
            vocab_db = arg
        elif opt == "--debug":
            debug = True
        else:
            usage()
            sys.exit()
         
    if not schema or not user or not password:
        usage()
        sys.exit(2)
    
    if not targetSchema:
        targetSchema = schema

    if not vocab_db:
        vocab_db = schema

    conn = None
    newLine = "\n"
    persistence_window =  1
    source_table = schema + ".encounter"
    target_table = targetSchema + ".longterm_era"

    time_begin = datetime.datetime.fromtimestamp(time.time())

    try:
     
        conn = psycopg2.connect( database="truven"
                                 , user=user
                                 , password=password
                                 , host="omop-datasets.cqlmv7nlakap.us-east-1.redshift.amazonaws.com"
                                 , port="5439"
                                 ) 
                

        read_cur = conn.cursor()
        insert_cur = conn.cursor()

      
        counter = 1
        new_table_name = "rx1"
         
        # Initial table determin drug_exposure_end_date
        # and replace drug concept with ingredients
        sql = "CREATE TEMPORARY TABLE " + new_table_name  + newLine \
            + "    AS " + newLine \
            + "SELECT DISTINCT ptid" + newLine \
            + "     , interaction_date AS start_date " + newLine \
            + "     , interaction_date AS end_date" + newLine \
            + "  FROM " + source_table  + newLine \
            + " WHERE visitID IS NULL " + newLine \
            + "   AND interaction_type = '" +  longTerm +"'" + newLine \
            + "   AND encId NOT IN " + newLine \
            + "     ( SELECT encId FROM " + targetSchema + ".enc_visit_map )" + newLine

        executeSQL( insert_cur, sql, debug )
        executeSQL( insert_cur, "commit", debug )

        while True:
            # start to reduce eras
            old_table_name = new_table_name
            counter += 1
            new_table_name = "rx" + str( counter )
            
            sql = "CREATE TEMPORARY TABLE " + new_table_name + newLine \
                + "    AS " + newLine \
                + "SELECT ptId, start_date , max( end_date ) AS end_date " + newLine \
                + "  FROM " + newLine \
                + "     ( SELECT ptId, min( start_date ) AS start_date, end_date " + newLine \
                + "         FROM " + newLine \
                + "            ( SELECT e.ptId " + newLine \
                + "                   , CASE WHEN e.start_date >  l.start_date " + newLine \
                + "                          THEN l.start_date " + newLine \
                + "                          ELSE e.start_date " + newLine \
                + "                     END AS start_date " + newLine \
                + "                   , CASE WHEN e.end_date > l.end_date " + newLine \
                + "                          THEN e.end_date " + newLine \
                + "                          ELSE l.end_date " + newLine \
                + "                     END AS end_date " + newLine \
                + "                FROM " + newLine \
                + "                   ( SELECT ptId, start_date, end_date " + newLine \
                + "                       FROM " + old_table_name + newLine \
                + "                   ) e " + newLine \
                + "                JOIN " + newLine \
                + "                   ( SELECT ptId, start_date, end_date " + newLine \
                + "                       FROM " + old_table_name + newLine \
                + "                   ) l " + newLine \
                + "                  ON l.ptId = e.ptId " + newLine \
                + "                 AND l.start_date <= e.end_date " + newLine \
                + "                 AND l.end_date + " + str( persistence_window ) + " >= e.start_date " + newLine \
                + "                 AND NOT( l.start_date = e.start_date AND l.end_date = e.end_date ) " + newLine\
                + "            ) " + newLine \
                + "        GROUP BY ptId, end_date " + newLine \
                + "     ) " + newLine \
                + " GROUP BY ptId, start_date" + newLine 

            executeSQL( insert_cur, sql, debug )
            executeSQL( insert_cur, "commit", debug )

            read_cur.execute( "SELECT count(*) FROM " + new_table_name )
            rows = read_cur.fetchone()

            if debug:
                print(  "%s: %d rows \n" % ( new_table_name, rows[0] ) )

            if rows[0] == 0:
                # reduced all the era, drop the last table
                sql = "INSERT INTO " + target_table + "( ptId, start_date, end_date ) " + newLine \
                    + "SELECT ptId, start_date, end_date " + newLine \
                    + "  FROM " + old_table_name + newLine

                executeSQL( insert_cur, sql, debug )
                executeSQL( insert_cur, "commit", debug )
                executeSQL( insert_cur, "DROP table " + old_table_name, debug )
                executeSQL( insert_cur, "DROP table " + new_table_name, debug )
                executeSQL( insert_cur, "commit", debug )
                break

            else:  # insert rows from old table not in new table

                sql = "INSERT INTO " + target_table + "( ptId, start_date, end_date ) " + newLine \
                    + "SELECT ptId,  start_date, end_date " + newLine \
                    + "  FROM " + old_table_name + newLine \
                    + " WHERE NOT EXISTS " + newLine \
                    + "     ( SELECT 'x' " + newLine \
                    + "         FROM " + new_table_name + newLine \
                    + "        WHERE " + new_table_name + ".ptId  = " + old_table_name + ".ptId  " + newLine \
                    + "          AND " + old_table_name + ".start_date " + newLine \
                    + "           <= " + new_table_name + ".end_date " + newLine \
                    + "          AND " + old_table_name + ".end_date " + newLine \
                    + "           >= " + new_table_name + ".start_date " + newLine \
                    + "     )"

                executeSQL( insert_cur, sql, debug )
                executeSQL( insert_cur, "commit", debug )

                executeSQL( insert_cur, "DROP table " + old_table_name, debug )
                executeSQL( insert_cur, "commit", debug )
#
# want to associate a single encounter with the era
#
            
        sql = "CREATE temporary table first_era_encounter " + newLine \
            + "AS" + newLine \
            + " SELECT ptId, start_date, encId " + newLine \
            + "   FROM " + newLine \
            + "      ( SELECT era.ptId, start_date, encId " + newLine \
            + "             , ROW_NUMBER() OVER( PARTITION BY era.ptId, interaction_date" + newLine \
            + "                                  ORDER BY interaction_timeStamp ) " + newLine \
            + "               AS rowNumber " + newLine \
            + "          FROM " + target_table + " era" + newLine \
            + "          JOIN " + source_table + " enc" + newLine \
            + "            ON enc.ptId = era.ptId " + newLine \
            + "           AND enc.interaction_date = era.start_date" + newLine \
            + "         WHERE interaction_type = '" + longTerm + "'" + newLine \
            + "      )" + newLine \
            + " WHERE rowNumber = 1"

        executeSQL( insert_cur, sql, debug )
        executeSQL( insert_cur, "commit", debug )

        # update first encounter


        sql = "UPDATE " + target_table + newLine \
            + "   SET first_enc " + newLine \
            + "     = ( SELECT encId" + newLine \
            + "           FROM first_era_encounter enc " + newLine \
            + "          WHERE enc.ptId = " + target_table + ".ptId" + newLine \
            + "            AND enc.start_date = " + target_table + ".start_date" + newLine \
            + "       )"

        executeSQL( insert_cur, sql, debug )
        executeSQL( insert_cur, "commit", debug )

        time_end = datetime.datetime.fromtimestamp(time.time())
        print( "Elapsed time: " + str( time_end - time_begin) )

    except psycopg2.DatabaseError, e:
        print( 'Error %s' % e )
        if conn:
            conn.close()
        sys.exit(1)

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])
