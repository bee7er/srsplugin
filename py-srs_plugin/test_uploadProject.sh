#!/bin/bash

# Change to the source directory
cd "/Users/brianetheridge/Library/Preferences/Maxon/Maxon Cinema 4D 2023_3BE69839/plugins/py-srs_plugin/projects/with_assets/c4dproject"

# Zip up the project file before uploading it
# The -C option changes the working directory, so that we don't tar up the entire directory structure

tar -zcvf "climatezilla_MAIN_03_srsTest.c4d.gz" --exclude=climatezilla_MAIN_03_srsTest.c4d.gz --exclude=.DS_Store -C "/Users/brianetheridge/Library/Preferences/Maxon/Maxon Cinema 4D 2023_3BE69839/plugins/py-srs_plugin/projects/with_assets/c4dproject" .

# Now upload the zipped file to the master
curl -F "upload=@climatezilla_MAIN_03_srsTest.c4d.gz" -H "Content-Type: multipart/form-data" -X POST "https://3n3.477.mywebsitetransfer.com/projects?email=contact_bee@yahoo.com&apiToken=fl9ltqesXqPi4EkSj8M498ZBYYq3WOcCCZ1A9fDYQlbeNEmdzyyf2rGFpNR0gDGB7IswfX3pRSLuoDBF&renderId=169"

# Go back to previous directory
cd -

exit