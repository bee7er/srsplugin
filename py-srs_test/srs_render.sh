#!/bin/bash

# Run render in the background
# $1 - c4dCommandLineExecutable location
# $2 - c4dProjectDir location
# $3 - from frame number
# $4 - to frame number

# Render the frames
nohup "$1" -nogui -render "$2/RenderTest.c4d" -frame "$3" "$4" -oimage "$2/RenderTest.c4d" -threads 0 &

exit
