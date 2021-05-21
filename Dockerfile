FROM python:3.9.0-alpine

USER root
WORKDIR /app

RUN apk add build-base mariadb-dev mariadb-client postgresql-dev

RUN pip install pipenv 

COPY ./Pipfile ./Pipfile.lock /app/

RUN echo "pipenv about to sync..."
RUN pipenv sync --dev --clear

COPY . /app/
EXPOSE 5000
