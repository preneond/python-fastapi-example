# Simple FastAPI Server Application

This project is FastAPI server application that simple performs two different tasks.

## Dependencies to install

- [Python 3.9](https://www.python.org/downloads/)
- [Pip](https://pypi.org/project/pip/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)


## Repo Config

To prevent syntax errors and keep high code quality, pre-commit hooks are used. They automatically check the code and clean it.

When the code is pushed to `origin/main` branch, the Github Action is triggered. It runs basic format checking, code linting, and functionality testing using pytest. All the config is in the `./setup.cfg` file.


## Setup

In order to run the server application locally, you need to fill in the secrets (they are not published to github due to security reasons).

The secrets to fill in are located in these files:

- `appsettings.yaml`
- `docker-compose.yaml`

To run the application in docker, run the following command:

```bash
docker-compose up
```

In order to run the application locally (for development purposes), you need to set `localhost` value to `db_connection.postgres_server` in `appsettings.yaml` file. Then you can run the following command.

```bash
docker run -d -p 5432:5432 -e POSTGRES_USER=xxx -e POSTGRES_PASSWORD=xxx -e POSTGRES_SERVER=xxx -e POSTGRES_DB=xxx postgres:14.2
python src/main.py
```

## XML/JSON Conversion

The first task aims to convert XML/JSON files.

The requests accept the multipart/form-data as an input with key `file` . The following endpoints are exposed:

* `[POST] /json2xml`: converts JSON to XML.
    * If `Accept` header is set to `text/xml`, the response will be in XML format, JSON otherwise.
    * if file's content-type is not `application/json`, the request will be rejected.

* `[POST] /xml2json`: converts XML to JSON
  * if file's content-type is not `text/xml`, the request will be rejected.

Additionally, the functionality can be tested via browser by using index template page that contains two forms.

The template page is accessible on root path `/`.


## Databases

The second task aims to demonstrate database operations.

    * `[GET] /user?email=<email_address>`: returns user's value
    * `[POST] /user?email=<email_address>`: creates new user with given value. If the user already exists, it updates the value.
    * `[DELETE] /user?email=<email_address>`: deletes user and the value
    * `[GET] /users`: returns all users and their values. The users are alphabetically sorted.
        * it accepts optional arguments `limit` and `offset` to limit the number of users and offset the users.


**Note:** More details about exposed endpoints can be found in the `/docs` REST API swagger.


## Testing

For testing purposes, [Pytest](https://docs.pytest.org/en/latest/getting-started.html) is used. All the tests are located in `./tests` folder
It is advised to run the firsts before commit to verify the application functionality (tests are not included in pre-commit hooks).

## Requirements
The project uses Python 3.9 (the latest version). This is a list of required libraries:
```python
fastapi==0.75.2
uvicorn==0.17.6
psycopg2-binary==2.9.3
python-dotenv==0.20.0
python-multipart==0.0.5
lxml==4.8.0
PyYAML==6.0
aiofiles==0.8.0
jinja2==3.1.2
email-validator==1.2.1
# dev requirements
mypy==0.950
flake8==4.0.1
autoflake==1.4
pre-commit==2.18.1
isort==5.10.1
pytest==7.1.2
pytest-cov==3.0.0
pytest-postgresql==4.1.1
pytest-asyncio==0.18.3
types-psycopg2==2.9.13
types-lxml==2022.4.10
types-PyYaml==6.0.7
black==22.3.0
psycopg==3.0.12
```

## License

This project is licensed under the terms of the MIT license.

