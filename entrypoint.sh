#!/bin/sh

python manage.py migrate
python seed_demo.py

exec "$@"