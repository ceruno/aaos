# Install

!!! warning "Use TLS"

    This installation routine does not provide any TLS configuration. We strongly recommend putting the endpoints behind a reverse proxy or web application firewall.

## Prerequisites

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## From GitHub

First clone the repository from github

``` sh
git clone https://github.com/ceruno/aaos.git
```

Create a .env file from the template

``` sh
cd aaos
mkdir .env
cp .env.example ./.env/.prod
```

Run the installer. This will create the db and tables in postgres and the admin user

``` sh
./install.sh
```

## From Docker Hub

create an `.env` file

```
SECRET_KEY=''
DJANGO_ALLOWED_HOSTS=*
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=''
DJANGO_SUPERUSER_EMAIL=''
ENCRYPTION_KEY=''

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=aaos
SQL_USER=aaos
SQL_PASSWORD=''
SQL_HOST=db
SQL_PORT=5432

POSTGRES_DB=aaos
POSTGRES_USER=aaos
POSTGRES_PASSWORD=''

CELERY_BROKER=redis://broker:6379/0
CELERY_BACKEND=redis://broker:6379/0

ELASTIC_APM_SERVICE_NAME=aaos
ELASTIC_APM_VERIFY_SERVER_CERT=True
ELASTIC_APM_LOG_LEVEL=error
ELASTIC_APM_DEBUG=False
ELASTIC_APM_SERVER_URL=
```

create a file called `docker-compose.yml` in the same directory

``` yaml
version: '3.4'

services:
  api:
    image: ceruno/aaos
    ports:
      - 8000:8000
    env_file:
      - .env
    depends_on:
      - broker
      - db
  db:
    image: postgres:15-alpine
    volumes:
      - db_data:/var/lib/postgresql/data/
    env_file:
      - .env
  broker:
    image: redis:7-alpine
  worker:
    image: ceruno/aaos
    command: ["celery", "-A", "api", "worker", "--loglevel=info"]
    env_file:
      - .env
    depends_on:
      - broker
  scheduler:
    image: ceruno/aaos
    command: ["celery", "-A", "api", "beat", "--loglevel=info", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"]
    env_file:
      - .env
    depends_on:
      - broker
  monitor:
    image: ceruno/aaos
    ports:
      - 5555:5555
    command: ["celery", "-A", "api", "flower", "--port=5555"]
    env_file:
      - .env
    depends_on:
      - broker
  web:
    image: ceruno/aaos-web
    ports:
      - 80:80
    depends_on:
      - api

volumes:
  db_data:
```

Start the containers, create the database and the superuser

``` bash
docker compose up -d
docker exec aaos-api-1 python manage.py makemigrations config
docker exec aaos-api-1 python manage.py migrate
docker exec aaos-api-1 python manage.py createsuperuser --noinput
```

