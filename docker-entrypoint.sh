#!/bin/sh

# before you start an app with gunicor, upgrade the db
# to latest revision in alembic
flask db upgrade

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"