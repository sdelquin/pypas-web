FROM python:3

WORKDIR /home/pytest

RUN pip install pytest

ENTRYPOINT ["pytest"]
