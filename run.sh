#!/bin/bash

cd $(dirname $0)
source ~/.pyenv/versions/pypas-web/bin/activate
exec gunicorn -b unix:/tmp/pypas-web.sock pypas.wsgi:application
