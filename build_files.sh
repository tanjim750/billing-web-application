#!/bin/bash

echo "BUILD START"
# Install dependencies
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
# Run collectstatic to collect all static files
python3 manage.py collectstatic --noinput --clear

echo "BUILD END"
