#!/bin/bash

# $1 - c4dProjectWithAssets
# $2 - the frame file name to download
# $3 - the location for the file that is downloaded - NOT USED
# $4 - the location for the frames
# $5 - the location for the psds - NOT USED
# $6 - srsDomain
# $7 - apiToken

echo "Downloading the frame result file"
echo "Processing $1 frame: $2 to location: $4"

# Change to the target directory
cd "$4"

# Now download the rendered file from the master to target directory
echo "URL: $6/uploads/$7/renders/$2"
echo "TO: ./$2"
curl --output "./$2" $6/uploads/$7/renders/$2

# Go back to previous directory
cd -

exit