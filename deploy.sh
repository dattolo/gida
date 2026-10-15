#!/usr/bin/env bash
# Run on PythonAnywhere from a Bash console: ./deploy.sh
set -euo pipefail
cd "$(dirname "$0")"
git pull --ff-only
source ~/.virtualenvs/gida/bin/activate
pip install --no-cache-dir -q -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput -v0
touch /var/www/gida_eu_pythonanywhere_com_wsgi.py
echo "Deploy OK"
