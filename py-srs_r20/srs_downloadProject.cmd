
:: %1: the file name of the project with assets file
:: %2: the download location for that file
:: %3: srsDomain

:: Testing:
:: srs_downloadProject.cmd RedshiftTestBe.c4d "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\downloads" http://3n3.477.mywebsitetransfer.com

@echo "Downloading the project with assets file"
@echo "Project with assets name: %1 and location: %2"

:: Save the current directory
@pushd .

:: Change to the source directory
@cd "%2"

:: Now download the zipped file from the master
curl --output %1.gz "%3/uploads/projects/%1.gz"

:: Unzip the project file before use
tar -xf %1.gz

:: Go back to previous directory
@popd

@exit