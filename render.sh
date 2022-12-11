#!/bin/bash

echo "Running render for $0 $1"

# Delete the completion file if it exists
rm -f /Users/brianetheridge/Code/srstest/actionCompleted.txt

# NB Since R21 you have to login to the command line every now and again:
#       Commandline.exe g_licenseUsername=<your_user_name> g_licensePassword=<your_password>

# Submit the render command to background, and note how we create the completion file afterwards
nohup /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline \
        -render ~/Code/srstest/srs/RedshiftTestBe.c4d \
        -frame 0 20 \
        -oimage ~/Code/srstest/srs/redshifttest/frames/RedshiftTestBe \
        -omultipass ~/Code/srstest/srs/redshifttest/psds/RedshiftTestBe \
         PNG; \
        touch /Users/brianetheridge/Code/srstest/actionCompleted.txt &

tar -zcvf ~/Code/srstest/srs/redshifttest/tars/RedshiftTestBePngs.tar.gz ~/Code/srstest/srs/redshifttest/frames
tar -zcvf ~/Code/srstest/srs/redshifttest/tars/RedshiftTestBePsds.tar.gz ~/Code/srstest/srs/redshifttest/psds

exit
