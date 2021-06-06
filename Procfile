release: python manage.py migrate
migrate: bash deployment.sh
web: gunicorn GoPus.wsgi --log-file -
