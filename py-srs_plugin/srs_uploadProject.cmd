
:: %1: the file name of the project with assets file
:: %2: the location of that file
:: %3: srsDomain
:: %4: email
:: %5: userToken
:: %6: renderId
:: %7: teamToken

@echo "Uploading the project with assets file to: %~3/projects"
@echo "Project with assets name: %~1 and location: %~2"

:: Save the current directory
@pushd .

:: Change to the source directory
@cd "%~2"

:: Zip up the project file before uploading it
:: The -C option changes the working directory, so that we don't tar up the entire directory structure
tar -zcvf "%~1.gz" --exclude="%~1.gz" -C "%~2" .

:: Now upload the zipped file to the master
curl -F "upload=@%~1.gz" -H "Content-Type: multipart/form-data" -X POST "%~3/projects?email=%~4&userToken=%~5&renderId=%~6&teamToken=%~7"

:: Go back to previous directory
@popd

@exit