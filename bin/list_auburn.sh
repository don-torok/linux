#!/bin/bash

# Create a snapshot of the volume, with description [Mon-Sun]: Weekly Backup for InstanceId (VolID VolumeId)
# also deletes the prior snapshot for that day of the week, keeping a 6 day window of backups
# D. Torok  - copied from example on the web

# Volume, instance and device, changes with instance
export INSTANCE=i-dda65ab8
export VOLUME=vol-658c9a08
export DEVICE=xvdi

#!/usr/bin/bash
export myHome=/home/dtorok
export EC2_HOME=/usr/local/ec2-api-tools
export PATH=$PATH:/usr/local/ec2-api-tools/bin
export JAVA_HOME=/usr/java/jre1.6.0_22

export EC2_PRIVATE_KEY=${myHome}/.ssh/pk-omop-prod.pem
export EC2_CERT=${myHome}/.ssh/cert-omop-prod.pem

# Set today's day of week parameter
dateDOW=`date | awk '{printf "%s %s%s", $1,$2,$3}'`
DOW=`echo ${dateDOW} | awk '{print $1}'`
echo $DOW
echo $dateDOW

# Create a file with old scheduled snapshots using same day of week parameter
# must be before creation or will delete the snapshot just created
ec2-describe-snapshots|egrep "Weekly Backup for $INSTANCE" 
