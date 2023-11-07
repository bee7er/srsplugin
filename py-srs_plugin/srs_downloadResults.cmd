
:: %1 - c4dProjectWithAssets
:: %2 - the frame file name to download
:: %3 - the location for the frames
:: %4 - srsDomain
:: %5 - apiToken
:: %6 - renderId

@echo "Downloading the frame range result file"
@echo "Processing %~1 frame: %~2 to location: %~3"

:: Save the current directory
@pushd .

:: Change to the target directory
@cd "%~3"

# Now download the rendered file name from the master to target directory
curl --output "./%~2" "%~4/uploads/%~5/renders/%~6/%~2"

:: Go back to previous directory
@popd

@exit