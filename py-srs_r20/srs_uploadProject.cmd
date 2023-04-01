
:: %1: the file name of the project with assets file
:: %2: the location of that file
:: %3: srsDomain

@echo "Uploading the project with assets file"
@echo "Project with assets name: %1 and location: %2"

:: Save the current directory
@pushd .

:: Change to the source directory
@cd "%2"

:: Zip up the project file before uploading it
gzip --best %1

:: Now upload the zipped file to the master
curl -v -F "upload=@%1.gz" -H "Content-Type: multipart/form-data" %3\projects

:: Go back to previous directory
@popd

exit