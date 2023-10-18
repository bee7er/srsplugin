
:: Uploading an image to the server
:: %1 - email
:: %2 - apiToken
:: %3 - fileToUpload
:: %4 - submittedByUserApiToken
:: %5 - framesDir
:: %6 - srsDomain

curl -F email=%1 -F apiToken=%2 -F submittedByUserApiToken=%4 -F "upload=@%3" -H "Content-Type: multipart/form-data" %6/results

echo "Uploaded %3"

exit
