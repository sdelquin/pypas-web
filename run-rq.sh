#!/bin/bash

cd $(dirname $0)
source ~/.pyenv/versions/pypas-web/bin/activate
exec python manage.py rqworker
