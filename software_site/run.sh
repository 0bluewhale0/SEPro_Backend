#!/bin/bash
sudo date -s "05:30:00"
# eval "conda activate soft_back_django"
# python manage.py runserver 101.42.40.112:8080
python manage.py runserver 0.0.0.0:8080 --verbosity 3