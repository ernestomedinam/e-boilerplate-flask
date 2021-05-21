#!/bin/sh
if [ ! -d './migrations' ] 
then
    docker-compose exec web pipenv run init
    echo "migrations folder created for travis..."
fi

docker-compose exec web pipenv run migrate
docker-compose exec web pipenv run upgrade

echo "db up to date, running tests"

docker-compose exec web pipenv run test

exit 0
