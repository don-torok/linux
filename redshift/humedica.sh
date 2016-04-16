#!/bin/bash

extension="newExt"

for zipFile in `ls *.sql`
do
   #get name without extension
   file="${zipFile%.*}"
   #strip path
   file=${file##*/}
   echo ${file}

   ## unzip zipFile
   if ! unzip ${zipFile}; then
       printf '%s\n' 'unzip failed for '${zipFile} >&2
       exit 1
   fi
   

   ## decrypt
   if ! decrypt ${file}"."${extension}; then  Q
       printf '%s\n' 'decrypt failed for '${file}"."${extension} >&2
       exit 1
   fi

   ## gzip
   if ! gzip ${file}"."${extension}; then
       printf '%s\n' 'gzip failed for '${file}"."${extension} >&2
       exit 1
   fi

done
