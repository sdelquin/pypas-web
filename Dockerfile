FROM python:3

# setup pytest user
RUN adduser --disabled-password --gecos "" --uid 7357 pytest
WORKDIR /home/pytest

# setup the python and pytest environments
RUN pip install \
    pytest

# setup entry point
USER pytest
ENTRYPOINT ["pytest"]
