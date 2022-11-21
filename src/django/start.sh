#!/bin/bash
#set -o errexit
#set -o pipefail
#set -o nounset
# . ./.env
# python manage.py makemigrations
# python manage.py migrate
gunicorn oar.wsgi --workers=2 --timeout=90 --log-level=debug --access-logfile=- --error-logfile=- --reload --bind 0.0.0.0:8081
