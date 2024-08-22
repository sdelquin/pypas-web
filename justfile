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

clean:
    #!/usr/bin/env bash
    find repository/ -name '*.pyc' -exec rm -f {} \;
    find repository/ -name '*.aux' -exec rm -f {} \;
    find repository/ -name '*.fdb_latexmk' -exec rm -f {} \;
    find repository/ -name '*.fls' -exec rm -f {} \;
    find repository/ -name '*.log' -exec rm -f {} \;
    find repository/ -name '*.out' -exec rm -f {} \;
    find repository/ -name '*.synctex.gz' -exec rm -f {} \;
    find repository/ -name '*.DS_Store' -exec rm -f {} \;
    find repository/ -name '_minted-*' -prune -exec rm -rf {} \;
    find repository/ -name '__pycache__' -prune -exec rm -rf {} \;
    find repository/ -name '.pytest_cache' -prune -exec rm -rf {} \;
    find repository/ -name '.mypy_cache' -prune -exec rm -rf {} \;
    find repository/ -name 'svg-inkscape' -prune -exec rm -rf {} \;

upload: clean
    rsync -avz --delete repository/ pypas.es:~/code/pypas-web/repository/

deploy:
    #!/usr/bin/env bash
    source .venv/bin/activate
    git pull
    pip install -r requirements.txt
    python manage.py migrate
    npm install --no-audit --no-fund
    python manage.py collectstatic --no-input
    supervisorctl restart pypas-web
    supervisorctl restart pypas-rq

build exercise:
    #!/usr/bin/env bash
    cd repository/{{ exercise }}/docs
    pdflatex -shell-escape README.tex

build-all:
    #!/usr/bin/env bash
    for exercise in repository/*/
    do
        (cd $exercise/docs && pdflatex -shell-escape README.tex)
    done

sync: check-venv database
    #!/usr/bin/env bash
    ssh -T andor << EOF
        cd ~/code/pypas-web
        source .venv/bin/activate
        python manage.py backup -b ~/tmp/pypas-web/
    EOF
    scp andor:~/tmp/pypas-web/`date +%Y-%m-%d`/db.sql /tmp/pypas.sql
    ssh andor rm -rf ~/tmp/pypas-web/
    psql pypas < /tmp/pypas.sql
    rm /tmp/pypas.sql
    python manage.py reset_admin

get exercise:
    scp -r andor:~/code/pypas-web/repository/{{ exercise }} repository/

# Grab version of installed Python package
@req package:
    pip freeze | grep -i {{ package }}

build-pytest:
    docker build -t pytest .

rq: check-venv redis
    python manage.py rqworker

expand-vendor:
    #!/usr/bin/env bash
    for exercise_dir in ./repository/*
    do
        cp exercises/.template/vendor.py $exercise_dir
    done

[private]
check-venv:
    #!/usr/bin/env bash
    if [ -z $VIRTUAL_ENV ]; then
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

# Start redis server
[private]
redis:
    #!/usr/bin/env bash
    if [[ $(grep -i redis $(find . -name settings.py)) ]]; then
        if   [[ $OSTYPE == "linux-gnu"* ]]; then
            pgrep -x redis &> /dev/null || sudo service redis start
        elif [[ $OSTYPE == "darwin"* ]]; then
            pgrep -x redis &> /dev/null || (open /Applications/Redis.app && sleep 2)
        fi
    fi
