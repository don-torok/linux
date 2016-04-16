#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#  Execute sql command for a file
#  comment lines start with #
#
#  Revision Log
# Who	When		What
# dtk  08Jun2014        use ';' as command end
# dtk  20Jan2014	added logging to a file
# dtk  12Apr2015        remove timing for Optum add # and -- for comments           
#

import psycopg2
import sys
import getopt
#import timing
import re

def usage():
	print( 'executeSQL.py [--debug] --user <user> ' \
	+ '--password <password> --file fileToRun --log logfile [--continue_on_error]' )

def main( argv ):

	conn = None
	user      = 'dtorok'
	password  = 'password'
	database  = 'ims'
	host      = "rs-ims.cra03mppdtga.us-east-1.redshift.amazonaws.com"
	port      = "5439"
	runFile   = ''
	debug     = False
	log        = False
	logto     = ''
	continue_on_error = False

	try:
		opts, args = getopt.getopt( argv, "", ["debug", "user=", "password=", "file=" \
                                          , "log=", "continue_on_error"] )

	except getopt.GetoptError as err:
		print ( err )
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt == "--debug":
			debug = True
		elif opt == "--continue_on_error":
			continue_on_error = True
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
					, host=host
					, port=port
					) 
		conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) 
		cur = conn.cursor()
 		command = ''
		inComment = False
		for line in file.readlines():
			line_before_comment = ''
			line_after_comment = ''
			# blank line
			if line == '\n':
				continue
		
			# look for comments line starting with #
			if line.strip().find('#') == 0:
				continue
			
			# look for comments line starting with --
			if line.strip().find('--') == 0:
				continue
			
			# test for start of comment note continue to fall through with text after comment
			if not inComment:
				match = re.search( '(.*)/\*(.*)', line )
				if match is not None:
					inComment = True
					line_before_comment = match.group(1) 
                                        line = match.group(2);

			# in comment
			if inComment:
				match = re.search( '.*\*/(.*)', line )
				if match is not None:
					line_after_comment = match.group(1) #everything after
					inComment = False

					if not( line_before_comment or line_after_comment ) :
						continue
                                else: # may or may not have been something before start of comment on same line
                                        line = line_before_comment
							
			if line_before_comment or line_after_comment:
				line = line_before_comment + line_after_comment

			# carrot indicates end of command
			match = re.search( '(.*);$', line.strip() )
			if match is not None:
				command += match.group(1)

				if debug:
					print( 'execute: ' + command )
					
				if log:
					logfile.write( command + '\n' )
				try:
					cur.execute( command )  
				except psycopg2.DatabaseError, e:
					print 'Error %s' % e
					if continue_on_error:
						pass
					else:
						sys.exit(1)
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
#					logfile.write( 'Elapsed: ' +  timing.getElapsed() + '\n' )	
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
