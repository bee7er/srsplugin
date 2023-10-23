
:: %1 - c4dProjectWithAssets
:: %2 - the frame file name to download
:: %3 - the location for the frames
:: %4 - srsDomain
:: %5 - apiToken
:: %6 - renderId

:: Testing:
:: srs_downloadResults.cmd "c4dproject.c4d" "c4dproject0000.tif" "C:\Users\conta\AppData\Roaming\MAXON\Cinema 4D R20_4FA5020E\plugins\projects\frames" "https://3n3.477.mywebsitetransfer.com WxhtuADUQCA0LroDLF5OoFkPvXtQ9LEd8CosCnAvVcilB7ulxFqh5qiK1iMzmWrqCUwWzfSlNfSk1hRo

@echo "Downloading the frame range result file"
@echo "Processing %~1 frame: %~2 to location: %~3"

:: Save the current directory
@pushd .

:: Change to the target directory
@cd "%~3"

# Now download the rendered file name from the master to target directory
echo "URL: %~4/uploads/%~5/renders/%~6/%~2"
echo "TO: ./%~2"
curl --output "./%~2" %~4/uploads/%~5/renders/%~6/%~2

:: Go back to previous directory
@popd

@exit