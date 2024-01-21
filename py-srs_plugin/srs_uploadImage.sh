#!/bin/bash

# Uploading an image to the server
# $1 - email
# $2 - userToken
# $3 - fileToUpload
# $4 - submittedByUserToken
# $5 - framesDir
# $6 - srsDomain
# $7 - renderId
# $8 - teamToken

curl -F "upload=@$3" -H "Content-Type: multipart/form-data" -X POST "$6/results?email=$1&userToken=$2&renderId=$7&teamToken=$8&submittedByUserToken=$4"

exit
