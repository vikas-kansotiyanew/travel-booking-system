web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn travel_booking.wsgi --bind 0.0.0.0:$PORT --log-file -
