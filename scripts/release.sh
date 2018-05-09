#!/bin/sh
set -e
rm -rf dist
python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf dist
python3 setup.py bdist_wheel
python3 -m twine upload dist/
