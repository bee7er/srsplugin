#!/bin/bash

# $1: the file name of the project with assets file
# $2: the download location for that file
# $3: srsDomain
# $4: submittedByUserApiToken
# $5: renderId

echo "Downloading the project with assets file"
echo "Project with assets name: $1 and location: $2 for renderId $5"

# Change to the source directory
cd "$2"

# Now download the zipped file from the master
curl --output "$1.gz" "$3/uploads/$4/projects/$5/$1.gz"

# Unzip the project file before use
tar -xzvf "$1.gz"

# Go back to previous directory
cd -

exit