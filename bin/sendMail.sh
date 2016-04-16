#!/bin/bash

function sendMail { 
/bin/mail -s "$SUBJECT" "$TO" <<EOF
$1
Time: `date` 
EOF
} 
SUBJECT='Oracle Prod Status'
TO=torok@omop.org

