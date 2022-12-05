#!/bin/bash
######## To invoke python !/usr/bin/env python3
# Example
# nohup python /path/to/test.py &

echo "Running render for $0 $1"

#touch ~/Code/srstest/actionCompleted.txt
#exit(1)


# Submit the render to another process
##### nohup /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline -render ~/Code/srstest/srs/srs.c4d -frame 0 5 -oimage ~/Code/srstest/srs/frames/srs -omultipass ~/Code/srstest/test_mp -oformat TIFF; touch ~/Code/srstest/actionCompleted.txt &

# Delete the completion file if it exists
rm -f ~/Code/srstest/actionCompleted.txt

# Submit the render command to background, and note how we create the completion file afterwards
nohup /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline -render ~/Code/srstest/srs/RedshiftTestBe.c4d -frame 0 10 -oimage ~/Code/srstest/srs/redshifttest/frames/redshifttest -omultipass ~/Code/srstest/test_mp PNG; touch /Users/brianetheridge/Code/srstest/actionCompleted.txt &

exit(1)