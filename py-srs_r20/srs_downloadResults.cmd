
# $1 - c4dProjectWithAssets
# $2 - the frame range file to download
# $3 - the location for the file that is downloaded
# $4 - the location for the frames
# $5 - the location for the psds
# $6 - srsDomain

echo "Downloading the frame range result file"
echo "Processing $1 frame range: $2 to location: $3"

# Change to the target directory
cd "$3"

####srs_downloadResults.sh "RedshiftTestBeWA.c4d" "12-23" "/Users/brianetheridge/Library/Preferences/MAXON/Cinema 4D R20_7DE41E5A/plugins/projects/downloads"
####http://srsapi.test/uploads/renders/frames_12-23_RedshiftTestBeWA.c4d.tar.gz

# Now download the zipped file from the master
curl --output frames_$2_$1.tar.gz $6\uploads\renders\frames_$2_$1.tar.gz
curl --output psds_$2_$1.tar.gz $6\uploads\renders\psds_$2_$1.tar.gz

# Unzip the frame range file before use
tar -xzf frames_$2_$1.tar.gz -C "$4"
tar -xzf psds_$2_$1.tar.gz -C "$5"

# Go back to previous directory
cd -

exit