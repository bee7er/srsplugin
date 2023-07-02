#!/bin/bash

# $1: the file name of the project with assets file
# $2: the location of that file
# $3: srsDomain
# $4: email
# $5: apiToken

echo "Uploading the project with assets file to $3">>out.txt
echo "Project with assets name: $1 and location: $2">>out.txt

# Change to the source directory
cd "$2"

# Zip up the project file before uploading it
# The -C option changes the working directory, so that we don't tar up the entire directory structure

tar -zcvf $1.gz "$2/$1" -C "$2" .

echo "Uploading to: $3/projects"

# Now upload the zipped file to the master
curl -F email=$4 -F apiToken=$5 -F "upload=@$1.gz" -H "Content-Type: multipart/form-data" $3/projects

# Go back to previous directory
cd -

exit