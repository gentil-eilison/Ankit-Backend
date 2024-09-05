# ankit_api

API utilizada para centralizar recursos para aprendizagem de idiomas, specifically AI and Anki.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Configurações

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Comandos Básicos

### Configuração Inicial

- Ao baixar a aplicação, será necessário rodar os comandos:

```
$ python manage.py migrate`
$ python manage.py load_nationalities`
$ python manage.py load_languages`
$ python manage.py load_superuser`
```

Esses comandos, respectivamente, aplicam as migrações no banco de dados; carregam dados sobre nacionalidades, idiomas e cria um superusuário padrão para o administrador. A senha e e-mail dele podem ser encontrados no arquivo `load_superuser.py`. Também será necessário criar um arquivo `.env` utilizando o arquivo `.env-EXAMPLE` como exemplo.

- Para criar um novo superusuário, basta utilizar este comando:

      $ python manage.py createsuperuser

### Celery

Esta aplicação utiliza o celery como um _distributed task queue_, além de conter também tarefas periodicas pré-configuradas e também aquelas que serão configuradas pelo administrador para realização do _backup_ do banco de dados. Dessa forma, é necessário rodar tanto o _celery worker_, quanto o _celery_beat_.

### Rodando o projeto

Para rodar o projeto localmente sem utilizar o Docker, utilize estes comandos:

```
$ python manage.py runserver
$ celery -A config.celery_app worker --loglevel=INFO
$ celery -A config.celery_app beat --loglevel=INFO
```

Pronto!

Para rodar com o Docker, crie, na pasta raíz do projeto, uma pasta `.envs` e, dentro dela, uma pasta `.local`. Dentro da última pasta, você irá criar dois arquivos: (1) É o arquivo `.django`, no qual você irá inserir as variáveis de ambiente do contêiner do Django; (2) O arquivo `.postgres`, onde as as variáveis de configuração do banco estarão. Após isso, rode:

```
docker compose -f local.yml build
docker compose -f local.yml up
```

Pronto!
