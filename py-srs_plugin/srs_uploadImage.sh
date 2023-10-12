#!/bin/bash

# Run render in the background
# $1 - c4dCommandLineExecutable
# $2 - c4dProjectDir
# $3 - downloadPWADir
# $4 - c4dProjectWithAssets
# $5 - from
# $6 - to
# $7 - outputFormat     - NOT USED
# $8 - outputToFramesDir
# $9 - outputToPsdsDir     - NOT USED
# ${10} - srs domain url
# ${11} - email
# ${12} - apiToken
# ${13} - submittedByUserApiToken

# @see https://www.cineversity.com/wiki/Command_Line_Parameters/

# Delete the completion file if it exists
rm -f "$2/actionCompleted.txt"

# Render the frames, and note how we create the completion file afterwards
# nohup "$1" -render "$3/$4" -frame "$5" "$6" -oimage "$8/$4" -omultipass "$9/$4" "$7"; touch "$2/actionCompleted.txt" &
nohup "$1" -nogui -render "$3/$4" -frame "$5" "$6" -oimage "$8/$4" -threads 0; touch "$2/actionCompleted.txt" &

# We need access to parameters 10, 11, 12 and 13 and we are finished with 1, 2, 3 and 4.
# We use shift to discard the first 4 and get access to them.

'''
    NB Since R21 you have to login to the command line.
    Using command line options would be good:  Commandline g_licenseUsername=<your_user_name> g_licensePassword=<your_password>
    You may need to do this more than once.
    For testing access to the command line renderer run the commands below to output to the testRender.txt file.
    Use the command that is generated in terminal.
    Follow any instructions; you will need to respond to prompts for the first invocation of the command line render.

cd "$8"
echo "$1" -nogui -render "$3/$4" -frame "$5" "$6" -oimage "$8/$4" > "$2/testRender.txt"

:: Go back to original directory
cd -

exit
'''

shift
shift
shift
shift

# Send the results to the master
# Should be something like the following to send this user email address and apiToken, too:
#     curl -v -F key1=value1 -F upload=@localfilename URL

# Change to frames directory
cd "$4"
# Send the rendered frames individually
for FILE in *; do
    echo $FILE;
    curl -F email=$7 -F apiToken=$8 -F submittedByUserApiToken=$9 -F "upload=@$FILE" -H "Content-Type: multipart/form-data" $6/results
    echo "Uploaded $FILE"
done

cd -

# Change to psds directory
cd "$5"
# Send the rendered PSDs individually
for FILE in *; do
    echo $FILE;
    curl -F email=$7 -F apiToken=$8 -F submittedByUserApiToken=$9 -F "upload=@$FILE" -H "Content-Type: multipart/form-data" $6/results
    echo "Uploaded $FILE"
done

cd -

exit
