
# $1: the file name of the project with assets file
# $2: the location of that file
# $3: srsDomain

echo "Uploading the project with assets file"
echo "Project with assets name: $1 and location: $2"

# Change to the source directory
cd "$2"

# Zip up the project file before uploading it
gzip --best RedshiftTestBeWA.c4d

# Now upload the zipped file to the master
curl -v -F "upload=@$1.gz" -H "Content-Type: multipart/form-data" $3\projects

# Go back to previous directory
cd -

exit