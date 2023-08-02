#!/bin/bash

# Run render in the background
# $1 - c4dCommandLineExecutable
# $2 - c4dProjectDir
# $3 - downloadPWADir
# $4 - c4dProjectWithAssets
# $5 - from
# $6 - to
# $7 - outputFormat
# $8 - outputToFramesDir
# $9 - outputToPsdsDir
# ${10} - srs domain url
# ${11} - email
# ${12} - apiToken

# LOCAL:
srs_render.sh "/Applications/MAXON/Cinema 4D R20/Commandline.app/Contents/MacOS" \
    "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects" \
    "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/downloads" \
    "RedshiftTestBe.c4d" \
    "0" \
    "2" \
    PNG \
    "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/frames" \
    "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/psds" \
    http://srsapi.test \
    contact_bee@yahoo.com \
    fl9ltqesXqPi4EkSj8M498ZBYYq3WOcCCZ1A9fDYQlbeNEmdzyyf2rGFpNR0gDGB7IswfX3pRSLuoDBF

# WWW:
# srs_render.sh "/Applications/MAXON/Cinema 4D R20/Commandline.app/Contents/MacOS" "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects" "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/downloads" "RedshiftTestBe.c4d" "0" "2" PNG "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/frames" "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/psds" https://3n3.477.mywebsitetransfer.com contact_bee@yahoo.com fl9ltqesXqPi4EkSj8M498ZBYYq3WOcCCZ1A9fDYQlbeNEmdzyyf2rGFpNR0gDGB7IswfX3pRSLuoDBF
