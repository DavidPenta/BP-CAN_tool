#!/bin/sh

if [ "$DB_NAME" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "pg-db" 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


python manage.py migrate --noinput
python manage.py collectstatic --noinput

DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_1_PASSWORD python manage.py createsuperuser --username $SUPER_USER_1_NAME --email $SUPER_USER_1_EMAIL --noinput
DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_2_PASSWORD python manage.py createsuperuser --username $SUPER_USER_2_NAME --email $SUPER_USER_2_EMAIL --noinput


gunicorn CAN_tool_project.wsgi:application --bind 0.0.0.0:8000
