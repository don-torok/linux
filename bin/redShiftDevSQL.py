#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#  Execute sql command for a file
#  use # as first character 
#
#  Revision Log
# Who	When		What
# dtk		20Jan2014	added logging to a file
#

import psycopg2
import sys
import getopt
import timing

def usage():
	print( 'redShiftDevSQL.py [--debug] --user <user> ' \
	+ '--password <password> --file fileToRun --log logfile' )

def main( argv ):

	conn = None
	user      = ''
	password  = ''
	database  = 'omopdev'
	runFile   = ''
	debug     = False
	log       = False
	logto     = ''
	delimiter = '^'
	host      = "omop-rs-dev.cat5ur0p6375.us-east-1.redshift.amazonaws.com"
	port      = 5439
        
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

	try:
		logfile = open( logto, 'w' )
	except: 
		print( 'Failed to open log file' + logto )
		sys.exit(1)
	try:
     
		conn = psycopg2.connect( dbname=database
					, user=user
					, password=password
					, host=host
					, port=port
					) 
#    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) 
		cur = conn.cursor()
		command = ''
		for line in file.readlines():
			
			# blank line
			if line == '\n':
				continue
			
			# look for comments
			if line.strip().find('#') == 0:
				continue
			
			# carrot indicates end of command
			if line.strip().find(delimiter)  == 0:
				if len( command ) == 0:
					continue
				if debug:
					print( 'execute\n' + command )
					
					if log:
						logfile.write( command + '\n' )
													
				cur.execute( command )  
				# see if command returns a value
				try:
					for record in cur:
						for value in record:
							if debug:
								print( value)
							if log:
								logfile.write( str( value ) + '\n' )
				except:
					pass
					
				if log:
					logfile.write( 'Elapsed: ' +  timing.getElapsed() + '\n' )	
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
			
		if logfile:
			logfile.close()


if __name__ == "__main__":
	main(sys.argv[1:])
