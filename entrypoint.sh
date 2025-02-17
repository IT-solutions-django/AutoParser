#!/bin/sh

# echo "Waiting for Redis..."
# while ! nc -z redis 6379; do
#   sleep 0.5
# done
sleep 2
# echo "Redis is up!"

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

celery -A core worker -l info -P prefork &
celery -A core beat -l info &
celery -A core flower -l info &
gunicorn core.wsgi:application --bind 0.0.0.0:8000 &

wait