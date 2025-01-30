#!/bin/sh

flask db upgrate

exec gunicorn --bind 0.0.0.0 "app:create_app()"