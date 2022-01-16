#!/bin/env bash

set -e

read -r -p "This script requires root permissions, please acknowledge that it is being run as root. [y|N]: "
if ! [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Aborting"
    exit 1
fi

echo "Updating script permissions."
chmod u+x scripts/test_samples.py
chmod u+x scripts/sample_gen.py

echo "Linking to bin."
sudo ln scripts/test_samples.py /usr/local/bin/test_samples
sudo ln scripts/sample_gen.py /usr/local/bin/sample_gen

echo "Done, Enjoy :)"