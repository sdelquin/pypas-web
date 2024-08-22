#!/bin/bash

cd $(dirname $0)
source .venv/bin/activate
exec gunicorn -b unix:/tmp/pypas-web.sock main.wsgi:application
