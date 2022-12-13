#!/bin/bash

# Run render in the background
# $1 - the command line command, but not using it atm as would not work
# $2 - c4dProjectDir
# $3 - c4dProjectWithAssets
# $4 - from
# $5 - to
# $6 - outputFormat
# $7 - outputToFramesDir
# $8 - outputToPsdsDir

# Delete the completion file if it exists
rm -f /Users/brianetheridge/Code/srstest/actionCompleted.txt

# NB Since R21 you have to login to the command line every now and again:
#       Commandline.exe g_licenseUsername=<your_user_name> g_licensePassword=<your_password>

# Submit the render command to background, and note how we create the completion file afterwards
nohup /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline \
                -render ~/Code/srstest/srs/RedshiftTestBe.c4d \
                -frame $4 $5 \
                -oimage $7/RedshiftTestBe \
                -omultipass $8/RedshiftTestBe $6; touch $2/actionCompleted.txt &

tar -zcvf ~/Code/srstest/srs/redshifttest/tars/RedshiftTestBePngs.tar.gz ~/Code/srstest/srs/redshifttest/frames
tar -zcvf ~/Code/srstest/srs/redshifttest/tars/RedshiftTestBePsds.tar.gz ~/Code/srstest/srs/redshifttest/psds

exit
