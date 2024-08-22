#!/bin/bash

cd $(dirname $0)
source .venv/bin/activate
exec python manage.py rqworker
