.PHONY: help migrate migrations create-superuser shell test lint install build collectstatic \
        start-backend start-frontend run-telegram docker-up docker-down docker-logs docker-build render \
        install-backend install-frontend lint-backend lint-frontend test-backend

# Help
help:
	@echo "Команды make:"
	@echo "  make install            - Установить все зависимости"
	@echo "  make install-backend    - Установить только бэкенд зависимости"
	@echo "  make install-frontend   - Установить только фронтенд зависимости"
	@echo "  make lint               - Запустить все линтеры"
	@echo "  make lint-backend       - Запустить линтеры бэкенда"
	@echo "  make lint-frontend      - Запустить линтеры фронтенда"
	@echo "  make test               - Запустить все тесты"
	@echo "  make test-backend       - Запустить тесты бэкенда"
	@echo "  make build              - Собрать проект"
	@echo "  make collectstatic      - Собрать статические файлы"
	@echo "  make migrations         - Создать миграции"
	@echo "  make migrate            - Применить миграции"
	@echo "  make shell              - Открыть Django shell"
	@echo "  make create-superuser   - Создать суперпользователя"

# Installation
install: install-backend install-frontend

install-backend:
	uv sync --frozen

install-frontend:
	cd app/frontend && npm ci

# Build
build:
	cd app/frontend && npm run build

collectstatic:
	uv run python manage.py collectstatic --noinput --clear

# Database
migrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate

# Development servers
start-backend:
	uv run python manage.py runserver

start-frontend:
	cd app/frontend && npm run dev

run-telegram:
	uv run python manage.py run_listener

# Code quality
lint: lint-backend lint-frontend

lint-backend:
	uv run ruff check .

lint-frontend:
	cd app/frontend && npm run lint

# Testing
test: test-backend

test-backend:
	uv run python manage.py test --parallel

# Docker
docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-build:
	docker compose build

# Production
render:
	uv run gunicorn app.wsgi:application

# Development
create-superuser:
	uv run python manage.py createsuperuser

shell:
	uv run python manage.py shell
