#!/bin/bash

# $1 - c4dProjectWithAssets
# $2 - the frame range file to download
# $3 - the location for the file that is downloaded
# $4 - the location for the frames
# $5 - the location for the psds
# $6 - srsDomain
# $7 - apiToken

echo "Downloading the project with assets file"

srs_downloadResults.sh "RedshiftTestBe.c4d" \
    "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/downloads" \
    http://srsapi.test \
    fl9ltqesXqPi4EkSj8M498ZBYYq3WOcCCZ1A9fDYQlbeNEmdzyyf2rGFpNR0gDGB7IswfX3pRSLuoDBF