#!/bin/bash

# $1: the file name of the project with assets file
# $2: the download location for that file
# $3: srsDomain
# $4: submittedByUserApiToken

echo "Downloading the project with assets file"

srs_downloadProject.sh "RedshiftTestBe.c4d" \
    "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/downloads" \
    http://srsapi.test \
    fl9ltqesXqPi4EkSj8M498ZBYYq3WOcCCZ1A9fDYQlbeNEmdzyyf2rGFpNR0gDGB7IswfX3pRSLuoDBF