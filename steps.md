# Steps

1. install `pipenv python3.7 python3.7-dev pkg-config`
2. create pipenv: `$ pipenv --python 3.7`
3. install flask: `$ pipenv install Flask Flask-DotEnv pytest`
4. create folders **app_name, config, tests**
5. create `settings.py` file in **app_name** folder
6. create `.env` file next to **app_name** folder
7. create `app_config.py` in **config** folder
8. create `__init__.py` in **app_name** folder
9. create `run.py` next to **app_name** folder
10. create `conftest.py` next to **app_name** folder
11. write tests for config in `test_config.py` in **tests** folder
12. create **api** folder in **app_name** folder
13. create `__init__py` and `routes.py` in **api** folder
14. write tests for api in `test_api.py` in **tests** folder
