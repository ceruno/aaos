#!/bin/sh
docker compose up -d
docker exec aaos-api-1 python manage.py makemigrations config
docker exec aaos-api-1 python manage.py migrate
docker exec aaos-api-1 python manage.py createsuperuser --noinput