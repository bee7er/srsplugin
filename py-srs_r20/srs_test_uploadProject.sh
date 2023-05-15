#!/bin/bash

# $1: the file name of the project with assets file
# $2: the location of that file
# $3: srsDomain
# $4: email
# $5: apiToken

# Testing:
echo "Testing project upload"

srs_uploadProject.sh \
    RedshiftTestBe.c4d \
    "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/with_assets/RedshiftTestBe.c4d" \
    http://srsapi.test \
    contact_bee@yahoo.com \
    fl9ltqesXqPi4EkSj8M498ZBYYq3WOcCCZ1A9fDYQlbeNEmdzyyf2rGFpNR0gDGB7IswfX3pRSLuoDBF

echo "Test completed"
