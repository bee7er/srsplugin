
:: Run render in the background
:: %1 - c4dCommandLineExecutable
:: %2 - c4dProjectDir
:: %3 - downloadPWADir
:: %4 - c4dProjectWithAssets
:: %5 - from
:: %6 - to
:: %7 - outputFormat
:: %8 - outputToFramesDir
:: %9 - outputToPsdsDir
:: %10 - srs domain url - NB we have to SHIFT in order to access this parameter
:: %11 - email - NB we have to SHIFT in order to access this parameter
:: %12 - apiToken - NB we have to SHIFT in order to access this parameter
:: %13 - submittedByUserApiToken - NB we have to SHIFT in order to access this parameter

:: NB Here we are being passed 13 parameters.  We must shift them in order to be able to access those above 9, they are
::    then accessible as parameters 6, 7, 8 and 9
:: NB Adding the tilde to the variable reference removes any surrounding quotes

:: srs_render.cmd "C:\Program Files\Maxon Cinema 4D R21" "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects" "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\downloads" "RedshiftTestBe.c4d" "0" "8" PNG "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\frames" "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\psds" https://3n3.477.mywebsitetransfer.com betheridge@gmail.com WxhtuADUQCA0LroDLF5OoFkPvXtQ9LEd8CosCnAvVcilB7ulxFqh5qiK1iMzmWrqCUwWzfSlNfSk1hRo WxhtuADUQCA0LroDLF5OoFkPvXtQ9LEd8CosCnAvVcilB7ulxFqh5qiK1iMzmWrqCUwWzfSlNfSk1hRo

:: Delete the completion file if it exists
@del /Q "%~2\actionCompleted.txt"

:: Submit the render command to background, and note how we create the completion file afterwards
:: I think this is unnecessary:  start /B
:: "%~1" -nogui -render "%~3\%~4" -frame "%~5" "%~6" -oimage "%~8\%~4" -omultipass "%~9\%~4" "%~7" && dir > "%~2\actionCompleted.txt"
"%~1" -nogui -render "%~3\%~4" -frame "%~5" "%~6" -oimage "%~8\%~4" -threads 0 && dir > "%~2\actionCompleted.txt"

:: Save the current directory
@pushd .

'''
    NB Since R21 you have to login to the command line.
    Using command line options would be good:  Commandline.exe g_licenseUsername=<your_user_name> g_licensePassword=<your_password>
    You may need to do this more than once.
    For testing access to the command line renderer run the commands below to output to the testRender.txt file.
    Use the command that is generated in terminal.
    Follow any instructions; you will need to respond to prompts for the first invocation of the command line render.

cd "%~8"
echo "%~1" -nogui -render "%~3\%~4" -frame "%~5" "%~6" -oimage "%~8\%~4" > "%~2\testRender.txt"

:: Go back to original directory
@popd

exit
'''

:: We need access to parameters 10, 11, 12 and 13 and we are finished with 1, 2, 3 and 4.
:: We use shift to discard the first 4 and get access to them.
shift
shift
shift
shift

:: Change to the frames directory
@cd "%~4"
:: Send the rendered frames individually
for %%f in (.\*.*) do (
    set /p val=<%%f
    echo "fullname: %%f"
    echo "name: %%~nf"
    curl -F email=%7 -F apiToken=%8 -F submittedByUserApiToken=%9 -F "upload=@%%f" -H "Content-Type: multipart/form-data" %6/results
    echo "Uploaded %%f"
)


:: Change to the frames directory
@cd "%~5"
:: Send the rendered psds individually
for %%f in (.\*.*) do (
    set /p val=<%%f
    echo "fullname: %%f"
    echo "name: %%~nf"
    curl -F email=%7 -F apiToken=%8 -F submittedByUserApiToken=%9 -F "upload=@%%f" -H "Content-Type: multipart/form-data" %6/results
    echo "Uploaded %%f"
)

:: Go back to original directory
@popd

@exit
