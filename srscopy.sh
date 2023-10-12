#!/bin/bash

echo "Running copy to Code"

rsync -av /Users/brianetheridge/Library/Preferences/MAXON/Maxon\ Cinema\ 4D\ 2023_3BE69839/plugins/py-srs_plugin /Users/brianetheridge/Code/srsplugin --exclude projects

# rsync -av /Users/brianetheridge/Library/Preferences/MAXON/Maxon\ Cinema\ 4D\ 2023_3BE69839/plugins/py-srs_test /Users/brianetheridge/Code/srsplugin

echo "Done"

