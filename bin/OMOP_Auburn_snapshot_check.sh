#!/bin/bash

function sendMail { 
/bin/mail -s "$SUBJECT" "$TO" <<EOF
$1
Time: `date` 
EOF
} 
SUBJECT='OMOP Auburn Backup'
TO=torok@omop.org

#!/usr/bin/bash
export myHome=/home/dtorok
export EC2_HOME=/usr/local/ec2-api-tools
export PATH=$PATH:/usr/local/ec2-api-tools/bin
export JAVA_HOME=/usr/java/jre1.6.0_22

export EC2_PRIVATE_KEY=${myHome}/.ssh/pk-omop-prod.pem
export EC2_CERT=${myHome}/.ssh/cert-omop-prod.pem
export INSTANCE=i-dda65ab8


# Get todays date an confirm snap shot created
dateDOW=`date | awk '{printf "%s %s%s", $1,$2,$3}'`
found=`ec2-describe-snapshots|egrep "${dateDOW}: Weekly Backup for $INSTANCE" | wc -l`

if [ "$found" -ne "1" ]; then
   sendMail "Missing backup for ${dateDOW}"
   exit 1
fi

exit 0

