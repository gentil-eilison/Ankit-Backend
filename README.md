# Ankit API

Ankit API is the back-end system for the Ankit application, a website with the goal of helping students acquire foreign-language
vocabulary in an efficient way using evidence-based techniques and generative AI powers.

This project was built using Cookiecutter Django as boilerplate.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Initial Setup

- Run the following commands after downloading the application:

```
$ python manage.py migrate`
$ python manage.py load_nationalities`
$ python manage.py load_languages`
$ python manage.py load_superuser`
```

Those commands, respectively, run database migrations; load nationality and language database data and creates a default superuser for administration tasks. Both the e-mail and password can be found on the `load_superuser.py` file. You'll need to create a `.env` fil as well based on the `.env-EXAMPLE` file.

- To create a new superuser, use the following comand:

      $ python manage.py createsuperuser

### Celery

This application uses Celery as a distributed task queue, containing periodic pre-configured periodic tasks and also the ones set up by the administrator for the database backup. Because of that, you'll need to run both celery worker and  celery_beat.

### Runing the Project
To run the project locally, without Docker, run these commands:

```
$ python manage.py runserver
$ celery -A config.celery_app worker --loglevel=INFO
$ celery -A config.celery_app beat --loglevel=INFO
```

Done!

To run the application with Docker, create, in the project's root folder, a folder named `.envs` and, and inside of it, another one named `.local`. In the `.local` folder, you'll need two files: (1)`.django`, containing Django's container environment variables; (2) `.postgres`, where PostgreSQL environment variables will be kept. After following those steps, run:

```
docker compose -f local.yml build
docker compose -f local.yml up
```

Done!

### API Docs
The documentation for the API can be found at [API Docs](http://localhost:<porta>/api/docs/) ou em [API Docs (Prod)](https://ankit.backend.gentil.dev.br/api/docs/)
