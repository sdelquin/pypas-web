alias mm := mmigrate

runserver: check-venv database
    python manage.py runserver

makemigrations app="": check-venv database
    python manage.py makemigrations {{ app }}

migrate app="": check-venv database
    python manage.py migrate {{ app }}

mmigrate app="": check-venv database
    python manage.py makemigrations {{ app }} && python manage.py migrate {{ app }}

showmigrations app="": database
    python manage.py showmigrations {{ app }}

su: check-venv
    python manage.py createsuperuser

startapp app: check-venv
    #!/usr/bin/env bash
    python manage.py startapp {{ app }}
    APP_CLASS={{ app }}
    APP_CONFIG="{{ app }}.apps.${APP_CLASS^}Config"
    perl -0pi -e "s/(INSTALLED_APPS *= *\[)(.*?)(\])/\1\2    '$APP_CONFIG',\n\3/smg" $(find . -name settings.py)

@sh:
    python manage.py shell

dbsh: database
    python manage.py dbshell

check:
    python manage.py check

# Grab version of installed Python package
@req package:
    pip freeze | grep -i {{ package }}

[private]
check-venv:
    #!/usr/bin/env bash
    if [ -z $VIRTUAL_ENV ] && [[ $(pyenv version-name) =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo You must activate a virtualenv!
        exit 1
    fi

# Start database server
[private]
database:
    #!/usr/bin/env bash
    if [[ $(grep -i postgres $(find . -name settings.py)) ]]; then
        if   [[ $OSTYPE == "linux-gnu"* ]]; then
            pgrep -x postgres &> /dev/null || sudo service postgresql start
        elif [[ $OSTYPE == "darwin"* ]]; then
            pgrep -x postgres &> /dev/null || (open /Applications/Postgres.app && sleep 2)
        fi
    fi
