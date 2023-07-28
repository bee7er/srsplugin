
:: %1 - c4dProjectWithAssets
:: %2 - the frame range file to download
:: %3 - the location for the file that is downloaded
:: %4 - the location for the frames
:: %5 - the location for the psds
:: %6 - srsDomain
:: %7 - apiToken

:: Testing:
:: srs_downloadResults.cmd "RedshiftTestBe.c4d" "0-8" "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\downloads" "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\frames" "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\psds" https://3n3.477.mywebsitetransfer.com WxhtuADUQCA0LroDLF5OoFkPvXtQ9LEd8CosCnAvVcilB7ulxFqh5qiK1iMzmWrqCUwWzfSlNfSk1hRo

@echo "Downloading the frame range result file"
@echo "Processing %~1 frame range: %~2 to location: %~4"

:: Save the current directory
@pushd .

:: Change to the target directory
@cd "%~4"

# Now download the rendered files from the master one at a time, all to target directory
echo "URL: %~6/uploads/%~7/renders/%~2"
echo "TO: ./%~2"
curl --output "./%~2" %~6/uploads/%~7/renders/%~2

:: Go back to previous directory
@popd

@exit