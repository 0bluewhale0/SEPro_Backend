#!/bin/bash
# sudo date -s "00:05:30"
sudo date -s '2023-06-17 01:05:30'
date
# eval "conda activate soft_back_django"
# python manage.py runserver 101.42.40.112:8080
python manage.py runserver 0.0.0.0:8080