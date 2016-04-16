#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#  Execute sql command for a file
#  comment lines start with #
#
#  Revision Log
# Who	When		What
# dtk  08Jun2014        use ';' as command end
# dtk  20Jan2014	added logging to a file
#

import psycopg2
import sys
import getopt
import datetime
import time
import re

def usage():
	print( 'executeSQL.py [--debug] --user <user> ' \
	+ '--password <password> --file fileToRun --log logfile' )

def main( argv ):

	conn = None
	user      = 'dtorok'
	password  = 'password'
	database  = 'truven'
	runFile   = ''
	debug     = False
	log        = False
	logto     = ''

	try:
		opts, args = getopt.getopt( argv, "", ["debug", "user=", "password=", "file=", "log="] )

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
		elif opt == "--file":
			runFile = arg    
		elif opt == "--log":
			log = True
			logto = arg
		else:
			usage()
			sys.exit()

	if not runFile or not user or not password:
		usage()
		sys.exit(2)

	try:
		file = open( runFile, 'r' )
	except:
		print( 'Failed to open ' + runFile )
		sys.exit(1)

	if log:
		try:
			logfile = open( logto, 'w' )
		except: 
			print( 'Failed to open ' + logto )
			sys.exit(1)
	try:
     
		conn = psycopg2.connect( database=database
					, user=user
					, password=password
					, host="omop-datasets.cqlmv7nlakap.us-east-1.redshift.amazonaws.com"
					, port="5439"
					) 
		conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) 
		cur = conn.cursor()
		command = ''
		for line in file.readlines():
			
			# blank line
			if line == '\n':
				continue
			
			# look for comments
			if line.strip().find('#') == 0 or line.strip().find('--') == 0:
				if debug:
					print( line )
				if log:
					logfile.write( line )
				continue
			
			# semi-colon indicates end of command
			match = re.search( '(.*);$', line.strip() )
			if match is not None:
				command += match.group(1)

				if debug:
					print( 'execute\n' + command )
					
				if log:
					logfile.write( command + '\n' )
										
				time_begin = datetime.datetime.fromtimestamp(time.time())
				cur.execute( command )
				time_end = datetime.datetime.fromtimestamp(time.time())

				rowcount = cur.rowcount;

				# see if command returns a value
				try:
					for row in cur.fetchall():
#						for value in record:
						if debug:
							print( row )
						if log:
							logfile.write( str( row ) + '\n' )
				except:
					pass
					
				if log:
					logfile.write( 'rows effected: ' + str( rowcount ) + '\n' )
					logfile.write( 'Elapsed: ' + str( time_end - time_begin)+'\n' )	
					logfile.flush()

				command = ''
				continue
			# keep building command	
			command += line
			
        
	except psycopg2.DatabaseError, e:
		print 'Error %s' % e    
		sys.exit(1)
    
	finally:
		if conn:
			conn.close()
		
		if file:
			file.close()
			
		if log:
			logfile.close()


if __name__ == "__main__":
	main(sys.argv[1:])
