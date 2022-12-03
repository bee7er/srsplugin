#!/bin/bash
######## To invoke python !/usr/bin/env python3
echo "Running render for $0 $1"

# Submit the render to another process
##### nohup /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline -render ~/Code/c4d/srs/srs.c4d -frame 0 5 -oimage ~/Code/c4d/srs/frames/srs -omultipass ~/Code/c4d/test_mp -oformat TIFF &

nohup /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline -render ~/Code/c4d/srs/RedshiftTest.c4d -oimage ~/Code/c4d/trendman/redshifttest/frames/redshifttest -omultipass ~/Code/c4d/test_mp PNG &

# Try adding a file to output to show completed

# Example
# nohup python /path/to/test.py &