#!/bin/bash

echo "Running copy to Code"

# cp -R /Users/brianetheridge/Library/Preferences/MAXON/Cinema\ 4D\ R20_7DE41E5A/plugins/py-srs_plugin/* /Users/brianetheridge/Code/srsplugin/py-srs_plugin/

rsync -av /Users/brianetheridge/Library/Preferences/MAXON/Maxon Cinema\ 4D\ 2023_3BE69839/plugins/py-srs_plugin /Users/brianetheridge/Code/srsplugin --exclude projects

rsync -av /Users/brianetheridge/Library/Preferences/MAXON/Maxon Cinema\ 4D\ 2023_3BE69839/plugins/py-srs_test /Users/brianetheridge/Code/srsplugin

echo "Done"

