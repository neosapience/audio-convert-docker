#!/bin/sh
set -e

if [ "$1" = 'gunicorn' ]; then
    shift
    exec gunicorn wsgi --name=audio-convert --bind=0.0.0.0:80 --log-level=debug \
        --timeout=1800 --worker-class=gevent --workers=1 "$@"
fi

exec "$@"
