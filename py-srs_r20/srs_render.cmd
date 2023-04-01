
:: Run render in the background
:: %1 - c4dCommandLineDir
:: %2 - c4dProjectDir
:: %3 - downloadPWADir
:: %4 - c4dProjectWithAssets
:: %5 - from
:: %6 - to
:: %7 - outputFormat
:: %8 - outputToFramesDir
:: %9 - outputToPsdsDir
:: %10 - srs api url

:: Testing:
:: srs_render.cmd "C:\Program Files\Maxon Cinema 4D R21" "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects" "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\downloads" "RedshiftTestBeWA.c4d" "0" "8" PNG "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\frames" "C:\Users\Russ\AppData\Roaming\MAXON\Maxon Cinema 4D R21_64C2B3BD\plugins\projects\psds"

:: Delete the completion file if it exists
@del /Q "%2\actionCompleted.txt"

:: NB Since R21 you have to login to the command line every now and again:
::       Commandline.exe g_licenseUsername=<your_user_name> g_licensePassword=<your_password>

:: Submit the render command to background, and note how we create the completion file afterwards
start /B "%1\Commandline" -render "%3\%4" -frame "%5" "%6" -oimage "%8\%4" -omultipass "%9\%4" "%7" > null.txt & dir > "%2\actionCompleted.txt"

:: Zip up the results
tar -zcvf "%8\frames_%5-%6_%4.tar.gz" "%8"
tar -zcvf "%9\psds_%5-%6_%4.tar.gz" "%9"

:: Upload the zipped files to master
curl -F "upload=@%8\frames_%5-%6_%4.tar.gz" -H "Content-Type: multipart/form-data" %10/results
curl -F "upload=@%9\psds_%5-%6_%4.tar.gz" -H "Content-Type: multipart/form-data" %10/results

@exit
