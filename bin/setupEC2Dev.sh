#!/usr/bin/bash
EC2_PRIVATE_KEY=/home/dtorok/.ssh/pk-omop-dev.pem
export EC2_PRIVATE_KEY

EC2_CERT=/home/dtorok/.ssh/cert-omop-dev.pem
export EC2_CERT

export PATH=${PATH}:/usr/share/ec2
