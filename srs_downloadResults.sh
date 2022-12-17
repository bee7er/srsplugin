#!/bin/bash

# $1: the frame range file to download
# $2: the location for the file that is downloaded

echo "Downloading the frame range result file"
echo "Processing frame range: $1 to location: $2"

# Change to the target directory
cd "$2"

# Now download the zipped file from the master
curl --output $1.gz http://srsapi.test/uploads/results/$1.gz

# Unzip the frame range file before use
gunzip $1.gz

# Go back to previous directory
cd -

exit