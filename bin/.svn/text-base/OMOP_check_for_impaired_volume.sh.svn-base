#!/bin/bash

function sendMail { 
/bin/mail -s "$SUBJECT" "$TO" <<EOF
$1
Time: `date` 
EOF
} 
dateDOW=`date | awk '{printf "%s %s%s", $1,$2,$3}'`
SUBJECT="OMOP Production impaired volume found $dateDOW"
TO=torok@omop.org

export myHome=/home/dtorok
export EC2_HOME=/usr/local/ec2-api-tools
export PATH=$PATH:/usr/local/ec2-api-tools/bin
export JAVA_HOME=/usr/java/jre1.6.0_22

export EC2_PRIVATE_KEY=${myHome}/.ssh/pk-omop-prod.pem
export EC2_CERT=${myHome}/.ssh/cert-omop-prod.pem


# Check for impaired volume
ec2-describe-volume-status --filter "volume-status.status=impaired" \
| egrep "^VOLUME[[:space:]]vol-" > impaired.temp

while read line
  do echo -e "$line\n"
  TO=torok@omop.org
  sendMail "$line"
  TO=mkhayter@gmail.com
  sendMail "$line"
done < impaired.temp

exit 0

