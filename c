#!/bin/bash

echo "Running copy from Code repository to Cinema 4D 2023 runtime instance"

rsync -av /Users/brianetheridge/Code/srsplugin/py-srs_plugin "/Users/brianetheridge/Library/Preferences/MAXON/Maxon Cinema 4D 2023_3BE69839/plugins"

echo "Done"

