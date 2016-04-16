#!/usr/local/bin/python
#-*- coding: utf-8 -*-
################################################################################
#  Convert vocabulary csv file into format accepted by BMS loader
#    1) replace comma separator with \xf2
#    2) remove quotes around text fields
#    3) remove trailing '|'
#
#  Change Log:
#  Who   When      What
#  dtk 04Jun2014   make target unicode
#  dtk 03Jun2014   Ignore imbedded carriage returns
#  dtk 02Jun2014   Open source as iso-8859-01
#   
#################################################################################
import codecs 
import argparse
import sys
import os.path
from io import open

def tell_me_about(s): return (type(s), s)


argParser = argparse.ArgumentParser(description='Convert vocabulary CSV file to BMS format' )
argParser.add_argument( 'source', help='file to convert' )


expected_fields = 0
fields = 0
rows = 0
bad = 0

init         = 1
quoted_field = 2
field        = 3
field_end    = 4
done         = 5

encoding_scheme = 'iso-8859-1'

carriage_return = unicode( chr( 13 ), encoding = encoding_scheme )
line_feed       = unicode( chr( 10 ), encoding = encoding_scheme )
args = argParser.parse_args()
source_file = args.source

if not os.path.isfile( source_file ):
    print( source_file + " not found." )
    sys.exit(1)

out_file = source_file.split( '.' )[0] + '.txt'
bad_file = source_file.split( '.' )[0] + '.bad'
log_file = source_file.split( '.' )[0] + '.log'

old_delimiter = ","
new_delimiter = unicode('\xf2', encoding_scheme)


try:
    f_out = codecs.open(out_file, mode="w+", encoding=encoding_scheme)
    f_bad = codecs.open(bad_file, mode="w+", encoding=encoding_scheme)
    f_log = codecs.open(log_file, mode="w+", encoding=encoding_scheme)

except:
    print( 'Problem opening output files' )
    sys.exit(1)

f_log.write( 'Conversion for ' + source_file + " to " + out_file + "\n" )

f = open( source_file, mode='r', encoding='iso-8859-1', newline=line_feed )

for line in f:
    line = line.strip()
    length = len(line)

    if length == 0:
        continue

    if line[length - 1 ] == '|':
        length = length - 1

#    print(line)
    i = 0
    fields = 0
    state = init
    target = u''

    while state <> done:
        if state == init:
            if i == length:
                state = field_end
            elif line[i] == '"':
                i = i + 1
                state = quoted_field
            else:
                state = field

        if state == quoted_field:
            if i == length:
                state = done
            elif line[i] == carriage_return:
                i = i + 1
                state = quoted_field
            elif line[i] == '"':
                i = i + 1
                if i == length or line[i] == old_delimiter:
                    state = field_end
                else: # this is quote within a field
                    target += line[i]
                    i = i + 1
                    state = quoted_field
            else:
                target += line[i]
                i = i + 1
                state = quoted_field

        if state == field:
            if i == length or line[i] == old_delimiter:
                state = field_end
            elif line[i] == carriage_return:
                i = i + 1
                state = field
            else:
                target += line[i]
                i = i + 1
                state = field

        if state == field_end:
            fields = fields + 1
            if i < length:
                i = i + 1
                target += new_delimiter
                state = init
            else:
                state = done;

        if state == done:
            rows = rows + 1
            if expected_fields == 0:
                expected_fields = fields

            if fields == expected_fields:
                f_out.write( target + "\n" )
            else:
                bad = bad + 1
                f_bad.write( "Row # " + "{:,}".format(rows) + "\n" ) 
                f_bad.write( line + "\n" )


f_log.write( '\tRows processed: ' + "{:,}".format(rows) + "\n" )
f_log.write( '\tColumns per row: ' + "{:,}".format(expected_fields) + "\n" )
f_log.write( '\tErrors:         ' + "{:,}".format(bad) + "\n" )

if bad == 0:
    os.remove( bad_file )

f_log.close()
f_out.close()
f_bad.close()
