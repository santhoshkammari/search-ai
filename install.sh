#!/bin/bash

set -e

python -m build

twine upload dist/*

pip uninstall -y inqs