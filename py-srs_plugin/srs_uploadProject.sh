#!/bin/bash

# $1: the file name of the project with assets file
# $2: the location of that file
# $3: srsDomain
# $4: email
# $5: apiToken

echo "Uploading the project with assets file to $3/projects"
echo "Project with assets name: $1 and location: $2"

# Testibng this script
# srs_uploadProject.sh RedshiftTestBe.c4d "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/with_assets/RedshiftTestBe.c4d" http://3n3.477.mywebsitetransfer.com contact_bee@yahoo.com fl9ltqesXqPi4EkSj8M498ZBYYq3WOcCCZ1A9fDYQlbeNEmdzyyf2rGFpNR0gDGB7IswfX3pRSLuoDBF

# Change to the source directory
cd "$2"

# Zip up the project file before uploading it
# The -C option changes the working directory, so that we don't tar up the entire directory structure

tar -zcvf $1.gz --exclude=$1.gz . -C "$2"

# Now upload the zipped file to the master
curl -F email=$4 -F apiToken=$5 -F "upload=@$1.gz" -H "Content-Type: multipart/form-data" $3/projects

# Go back to previous directory
cd -

exit