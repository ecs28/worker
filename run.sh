#!/usr/bin/env bash
echo 'Starting test'
echo ''
echo 'activating virtual env'
#activate venv
source ./venv/bin/activate

echo ''
# echo 'running tests'
# run unit tests
python3 cmd/instaworker.py

echo 'deactivate virtual env'
deactivate