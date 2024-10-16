#!/bin/bash

set -e

# Check if dist directory exists before deleting
if [ -d "dist" ]; then
    rm -r dist
fi

python -m build

twine upload dist/*

pip uninstall -y inqs