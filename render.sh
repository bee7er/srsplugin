#!/bin/bash

echo "Running render for $0 $1"

# Delete the completion file if it exists
rm -f ~/Code/srstest/actionCompleted.txt

# Submit the render command to background, and note how we create the completion file afterwards
nohup /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline \
        -render ~/Code/srstest/srs/RedshiftTestBe.c4d \
        -frame 0 10 \
        -oimage ~/Code/srstest/srs/redshifttest/frames/RedshiftTestBe \
        -omultipass ~/Code/srstest/srs/redshifttest/psds/RedshiftTestBe \
         PNG; \
        touch /Users/brianetheridge/Code/srstest/actionCompleted.txt &

tar -zcvf ~/Code/srstest/srs/redshifttest/tars/RedshiftTestBePngs.tar.gz ~/Code/srstest/srs/redshifttest/frames
tar -zcvf ~/Code/srstest/srs/redshifttest/tars/RedshiftTestBePsds.tar.gz ~/Code/srstest/srs/redshifttest/psds

exit(1)