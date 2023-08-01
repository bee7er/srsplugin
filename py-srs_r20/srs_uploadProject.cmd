
:: %1: the file name of the project with assets file
:: %2: the location of that file
:: %3: srsDomain
:: %4: email
:: %5: apiToken

:: Testing
:: srs_uploadProject.cmd "RedshiftTestBe.c4d" "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\with_assets\RedshiftTestBe.c4d" https://3n3.477.mywebsitetransfer.com

@echo "Uploading the project with assets file to: %~3/projects"
@echo "Project with assets name: %~1 and location: %~2"

:: Save the current directory
@pushd .

:: Change to the source directory
@cd "%~2"

:: Zip up the project file before uploading it
:: The -C option changes the working directory, so that we don't tar up the entire directory structure
tar -zcvf %~1.gz --exclude=%~1.gz . -C "%~2"

:: Now upload the zipped file to the master
curl -F email=%~4 -F apiToken=%~5 -F "upload=@%~1.gz" -H "Content-Type: multipart/form-data" %~3/projects

:: Go back to previous directory
@popd

@exit