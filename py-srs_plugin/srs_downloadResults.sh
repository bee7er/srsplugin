#!/bin/bash

# $1 - c4dProjectWithAssets
# $2 - the frame file name to download
# $3 - the location for the frames
# $4 - srsDomain
# $5 - apiToken

echo "Downloading the frame result file"
echo "Processing $1 frame: $2 to location: $3"

# Testibng this script
# srs_downloadResults.sh "RedshiftTestBe.c4d" "RedshiftTestBe0002.PNG" "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/frames" http://srsapi.test fl9ltqesXqPi4EkSj8M498ZBYYq3WOcCCZ1A9fDYQlbeNEmdzyyf2rGFpNR0gDGB7IswfX3pRSLuoDBF

# Change to the target directory
cd "$3"

# Now download the rendered file from the master to target directory
echo "URL: $4/uploads/$5/renders/$2"
echo "TO: ./$2"
curl --output "./$2" $4/uploads/$5/renders/$2

# Go back to previous directory
cd -

exit