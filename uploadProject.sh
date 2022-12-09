#!/bin/bash

# $1: the file name of the project with assets file
# $2: the location of that file

echo "Uploading the project with assets file"
echo "Project name: $1 and location: $2"

# Zip up the project file before uploading it
tar -zcvf $2$1.tar.gz $2$1.c4d

# Now upload the zipped file to the master
curl -v -F "upload=@$2$1.tar.gz" -H "Content-Type: multipart/form-data" http://srsapi.test/projects

exit