
:: Uploading an image to the server
:: %1 - email
:: %2 - apiToken
:: %3 - fileToUpload
:: %4 - submittedByUserApiToken
:: %5 - framesDir
:: %6 - srsDomain
:: %7 - renderId

curl -F "upload=@%~3" -H "Content-Type: multipart/form-data" -X POST "%~6/results?email=%~1&apiToken=%~2&renderId=%~7&submittedByUserApiToken=%~4"

exit
