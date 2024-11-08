# Launch Django development server
runserver: check-venv database
    python manage.py runserver

# Make migrations for single app or whole project
makemigrations app="": check-venv database
    python manage.py makemigrations {{ app }}

# Commit migrations for single app or whole project
migrate app="": check-venv database
    python manage.py migrate {{ app }}

alias mm := mmigrate

# Make migrations & Commit migrations (all in one)
mmigrate app="": check-venv database
    python manage.py makemigrations {{ app }} && python manage.py migrate {{ app }}

# Show migrations for single app or whole project
showmigrations app="": database
    python manage.py showmigrations {{ app }}

# Create superuser
su: check-venv
    python manage.py createsuperuser

# Add a new app (also writes in settings.py for INSTALLED_APPS)
startapp app: check-venv
    #!/usr/bin/env bash
    python manage.py startapp {{ app }}
    APP_CLASS={{ app }}
    APP_CONFIG="{{ app }}.apps.${APP_CLASS^}Config"
    perl -0pi -e "s/(INSTALLED_APPS *= *\[)(.*?)(\])/\1\2    '$APP_CONFIG',\n\3/smg" $(find . -name settings.py)

# Open a Django shell
@sh:
    python manage.py shell

# Open a database shell
dbsh: database
    python manage.py dbshell

# Check project
check:
    python manage.py check

# Clean all temporary files (including TEX)
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

# Upload exercises to production
upload:
    rsync -avz --delete --exclude-from rsync_exclude.txt repository/ pypas.es:~/code/pypas-web/repository/

# Deploy project to production
deploy:
    #!/usr/bin/env bash
    source .venv/bin/activate
    git pull
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py collectstatic --no-input
    supervisorctl restart pypas-web
    supervisorctl restart pypas-rq

# Build documentation (TEX) for single exercise
build exercise:
    #!/usr/bin/env bash
    cd repository/{{ exercise }}/docs
    pdflatex -shell-escape README.tex

# Build documentation (TEX) for all exercises
build-all:
    #!/usr/bin/env bash
    for exercise in repository/*/
    do
        (cd $exercise/docs && pdflatex -shell-escape README.tex)
    done

# Sync project from production: PRODUCTION ---> DEVELOPMENT
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

# Get a single exercise from production to development (inside repository)
get exercise:
    scp -r andor:~/code/pypas-web/repository/{{ exercise }} repository/

# Grab version of installed Python package
@req package:
    pip freeze | grep -i {{ package }}

# Build docker image for testing (pytest)
build-pytest:
    docker build -t pytest .

# Launch worker for Redis Queue (RQ)
rq: check-venv redis
    python manage.py rqworker

# Copy vendor.py to all exercise folders in repository
expand-vendor:
    #!/usr/bin/env bash
    for exercise_dir in ./repository/*
    do
        cp exercises/.template/vendor.py $exercise_dir
    done

# Show documentation for exercise
@doc exercise:
    open repository/{{ exercise }}/docs/README.pdf

# Get mark for a certain user & frame
@getmark context bucket user:
    ./manage.py get_mark {{ context }} {{ bucket }} {{ user }}

# Check if virtualenv is activated
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
