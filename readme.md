# Short links

REST API based on FastAPI for generate your own short links.


## Requirements

1. Docker
2. Docker-compose

For local development:

3. Poetry


## Before start

Put to project file .env with follow variables:

```bash
DOCKER_IMAGE_BACKEND=api

# Backend
HOST=localhost
PORT=80
DB_HOST=db
DB_NAME=links
DB_USER=admin
DB_PASSWORD=admin
TIME_CHECK_EXPIRED_LINKS_SECONDS=60
ACCESS_TOKEN_EXPIRE_MINUTES=3600
SHORT_LINK_EXPIRE_DAYS=1

# Postgres
POSTGRES_SERVER=db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=links

# PgAdmin
PGADMIN_LISTEN_PORT=5050
PGADMIN_DEFAULT_EMAIL=admin@admin.ru
PGADMIN_DEFAULT_PASSWORD=admin
```



## Start stack

```bash
sudo docker-compose up -d
```

After few minutes will build image for rest api server.
Also will pull images for other required services (PostgreSQL, pdAdmin)
And then api will accessible on http://localhost:8080/api
Documentation on http://localhost:8080/docs


## How to use

For create new user send POST request to http://localhost:8080/api/sign-up

For login send POST request to http://localhost:8080/api/token

For get user information send GET request to http://localhost:8080/api/users/me

For create short_link send POST request to http://localhost:8080/api/links

For redirect to long link send GET request to http://localhost:8080/{short_link}

How long links live defines by SHORT_LINK_EXPIRE_DAYS in .env file.

Every TIME_CHECK_EXPIRED_LINKS_SECONDS links with exrired datetime will be deleted.

By default new created link has SHORT_LINK_EXPIRE_DAYS life.

## Tests

For run test :

```bash
sudo docker-compose exec backend scripts/./start_tests.sh
```

For test pep8

```bash
sudo docker-compose exec backend flake8
```

## Developing

Just start stack :

```bash
sudo docker-compose up -d
```

And work with code in project. 
Inside the container "backend" works :

```bash
uvicorn --port 80 --host 0.0.0.0 main:app --reload
```
It will reload server when changes will be found

For read logs:

```bash
sudo docker-compose logs backend
```
