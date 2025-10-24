# Деплой на Render.com
Предварительные требования

    Аккаунт на render.com

    Репозиторий на GitHub

## 1. Подготовка файлов

Убедитесь, что в корне проекта есть следующие файлы:

build.sh

```
#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

make install && make build && make collectstatic && make migrate
```
Makefile
```
install:
    uv sync && cd app/frontend && uv run npm install

build:
    cd app/frontend && uv run npm run build

collectstatic:
    uv run manage.py collectstatic --noinput

migrate:
    uv run manage.py migrate

render:
    uv run gunicorn app.wsgi:application
```
## 2. Создание базы данных PostgreSQL

    В панели Render нажмите "+ New" → "Postgres"

    Заполните настройки:

        Name: your-db-service-name

        Database: your-db-name (или оставить пустым, будет сгенерирован)

        User: your-db-username (или оставить пустым, будет сгенерирован)

        Plan: Free (или выберите нужный план)

    После создания БД получите поля hostname, port, database, username, password из раздела "Connections"

## 3. Создание Web Service

    Нажмите "+ New" → "Web Service"

    Подключите ваш GitHub репозиторий

    Заполните настройки:

        Name: your-service-name

        Language: Python 3

        Branch: main (или ваша ветка)

        Build Command: chmod +x build.sh && ./build.sh

        Start Command: make render

        Instance Type: Free (или выберите нужный план)

    В разделе Environment Variables выберите Add from .env и добавьте:
```
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com

# Database (замените значения на актуальные из вашей БД Render)
DATABASE_NAME=your-db-name
DATABASE_USER=your-db-username
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=your-db-host
DATABASE_PORT=your-db-port
```
## 4. Деплой

    После создания сервиса Render автоматически запустит деплой

    Следите за процессом в реальном времени в логах

    После успешного деплоя приложение будет доступно по URL:
    https://your-service-name.onrender.com
