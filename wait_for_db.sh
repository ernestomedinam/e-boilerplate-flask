#!/bin/sh
echo "waiting for postgres to be ready..."

while ! nc -z app_db 5432 ; do sleep 10 ; done ;

echo "postgresql started..."

if [ ! -d "./migrations" ]
then
    echo "running migrations..."
    pipenv run init
fi

echo "upgrading db..."

pipenv run migrate
pipenv run upgrade

echo "db ready... launching app"

pipenv run start

exit 0
