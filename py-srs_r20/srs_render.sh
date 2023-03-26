#!/bin/bash

# Run render in the background
# $1 - c4dCommandLineDir
# $2 - c4dProjectDir
# $3 - downloadPWADir
# $4 - c4dProjectWithAssets
# $5 - from
# $6 - to
# $7 - outputFormat
# $8 - outputToFramesDir
# $9 - outputToPsdsDir
# $10 - srs api url

#srs_render.sh "/Applications/MAXON/Cinema 4D R20/Commandline.app/Contents/MacOS" "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects" "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/downloads" "RedshiftTestBeWA.c4d" "0" "8" PNG "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/frames" "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/psds"

# Delete the completion file if it exists
rm -f "$2/actionCompleted.txt"

# NB Since R21 you have to login to the command line every now and again:
#       Commandline.exe g_licenseUsername=<your_user_name> g_licensePassword=<your_password>

# Submit the render command to background, and note how we create the completion file afterwards
nohup "$1/Commandline" -render "$3/$4" -frame "$5" "$6" -oimage "$8/$4" -omultipass "$9/$4" "$7"; touch "$2/actionCompleted.txt" &

# Zip up the results
tar -zcvf "$8/frames_$5-$6_$4.tar.gz" "$8"
tar -zcvf "$9/psds_$5-$6_$4.tar.gz" "$9"
# Upload the zipped files to master
curl -F "upload=@$8/frames_$5-$6_$4.tar.gz" -H "Content-Type: multipart/form-data" $10/results
curl -F "upload=@$9/psds_$5-$6_$4.tar.gz" -H "Content-Type: multipart/form-data" $10/results

exit
