#!/bin/bash
# Install dependencies
pip install -r requirements.txt

python manage.py makemigrations
# Apply database migrations
python manage.py migrate
