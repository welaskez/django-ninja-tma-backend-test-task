#!/bin/sh

if [ "$SERVICE_TYPE" = "api" ]; then
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py runserver 0.0.0.0:8000
elif [ "$SERVICE_TYPE" = "bot" ]; then
    python -m bot
fi