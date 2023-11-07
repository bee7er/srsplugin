#!/bin/bash

# Change to the source directory
cd "/Users/brianetheridge/Library/Preferences/Maxon/Maxon Cinema 4D 2023_3BE69839/plugins/py-srs_plugin/projects/with_assets/ConeTest"

# Zip up the project file before uploading it
# The -C option changes the working directory, so that we don't tar up the entire directory structure

tar -zcvf "ConeTest.c4d.gz" --exclude=ConeTest.c4d.gz -C "/Users/brianetheridge/Library/Preferences/Maxon/Maxon Cinema 4D 2023_3BE69839/plugins/py-srs_plugin/projects/with_assets/ConeTest" .

# Now upload the zipped file to the master
curl -F "upload=@ConeTest.c4d.gz" -H "Content-Type: multipart/form-data" -X POST "http://srsapi.test/projects?email=contact_bee@yahoo.com&apiToken=fl9ltqesXqPi4EkSj8M498ZBYYq3WOcCCZ1A9fDYQlbeNEmdzyyf2rGFpNR0gDGB7IswfX3pRSLuoDBF&renderId=159"

# Go back to previous directory
cd -

exit