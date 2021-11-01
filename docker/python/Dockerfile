# syntax=docker/dockerfile:1.3.1-labs
FROM python:3.10.0-alpine

ENV PYTHONUNBUFFERED 1

RUN <<eof
    mkdir /src &&
    mkdir /tests &&
    mkdir /requirements &&
    mkdir -p /root/.cache/pip &&
    adduser --disabled-password --gecos '' keiyakusha
eof

WORKDIR /src

COPY requirements.txt requirements-dev.txt /requirements/

RUN \
    --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/etc/apk/cache \
<<eof
    apk add --virtual .build-deps \
        gcc \
        git \
        musl-dev \
        postgresql-dev \
    &&

    pip install -U pip &&
    pip install -r /requirements/requirements-dev.txt &&
    apk del .build-deps &&
    apk add libpq &&

    echo "built"
eof

USER keiyakusha
