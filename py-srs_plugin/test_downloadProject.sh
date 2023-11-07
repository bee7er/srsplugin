#!/bin/bash

# Change to the source directory
cd "/Users/brianetheridge/Library/Preferences/Maxon/Maxon Cinema 4D 2023_3BE69839/plugins/py-srs_plugin/projects/downloads"

# Now download the zipped file from the master
curl --output "ConeTest.c4d.gz" "http://srsapi.test/uploads/fl9ltqesXqPi4EkSj8M498ZBYYq3WOcCCZ1A9fDYQlbeNEmdzyyf2rGFpNR0gDGB7IswfX3pRSLuoDBF/projects/159/ConeTest.c4d.gz"

# Unzip the project file before use
tar -xzvf "ConeTest.c4d.gz"

# Go back to previous directory
cd -

exit