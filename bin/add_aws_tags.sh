#!/bin/bash
. /home/dtorok/bin/setupEC2Prod.sh

ec2-create-tags i-873031ed  --tag stack=Production --tag name=lsomop
ec2-create-tags i-66236509  --tag stack=Production --tag name=ccae
ec2-create-tags i-7fdd361c  --tag stack=Production --tag name=ccaeElt1
ec2-create-tags i-c037ebad  --tag stack=Production --tag name=SpotFire
ec2-create-tags i-2972074c  --tag stack=Production --tag name=MetaThesaurus
ec2-create-tags i-7dfb9718  --tag stack=Production --tag name=dtk_work
ec2-create-tags i-88e9f1e7  --tag stack=Production --tag name="Spotfire Web Player"
ec2-create-tags i-863465e9  --tag stack=Production --tag name="Web RL"
ec2-create-tags i-dda65ab8  --tag stack=Production --tag name="OMOP Auburn Prod"
ec2-create-tags i-a0a180c7  --tag stack=Production --tag name="mini-sentinel"
# This was my oracle test, stopped 1/7/2013
ec2-create-tags i-af5f1fcb  --tag stack=Production --tag name="FTP Server"
ec2-create-tags i-fd8dba8d  --tag stack=Production --tag name="SAS DTk"

# ec2-create-tags   --tag stack=Production --tag name=""



ec2-describe-tags --filter "resource-type=instance"

. /home/dtorok/bin/setupEC2Dev.sh

ec2-create-tags i-dbf255be  --tag stack=Production --tag name="DTk Test Oracle"
# stopped 1/7/2013
