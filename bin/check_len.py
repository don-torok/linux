#!/usr/local/bin/python
#
# Check the length of source code description
# in vocabulary file
#
#
lineCount = 0
maxLen = 256

# open file
csv=open("SOURCE_TO_CONCEPT_MAP.csv")
for l in csv.xreadlines():
    lineCount += 1
    # replace escaped comma with semicolon
    l.replace('\,', ';' )
    # break the line into pieces at the comma
    pieces = l.split(",")
    # description is the third piece
    desc = pieces[2]
    if len(desc) > maxLen:
        print( 'line: ' + str(lineCount ) + ' len: ' + str( len(desc) ) + '\n' )
        print( desc + '\n' )

csv.close()
