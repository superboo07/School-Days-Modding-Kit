#!/bin/bash

# Ensure the script is being run from within its directory
cd "$(dirname "$0")"

# Prompt the user to input the directory of their School Days install
read -p "Enter the directory of your School Days install: " install_dir
if [ ! -d "$install_dir" ]; then
    echo "Directory does not exist!"
    exit 1
fi

python ./src/modCUI.py "$install_dir"
exit 0