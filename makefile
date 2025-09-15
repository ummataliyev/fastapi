.PHONY: help build up down logs restart migrate clean disable-postgres disable-mysql disable-mongo

include .env
export $(shell sed 's/=.*//' .env)

help:
	@echo "Available commands:"
	@echo "  make build             - Build the Docker image"
	@echo "  make up                - Start FastAPI"
	@echo "  make down              - Stop and remove containers"
	@echo "  make logs              - View logs"
	@echo "  make restart           - Restart FastAPI"
	@echo "  make migrate           - Run Alembic migrations"
	@echo "  make clean             - Remove volumes and stop everything"
	@echo "  make disable-postgres  - Stop and remove PostgreSQL container"
	@echo "  make disable-mysql     - Stop and remove MySQL container"
	@echo "  make disable-mongo     - Stop and remove Mongo container"

build:
	@echo "🔨 Building FastAPI Docker image..."
	docker compose build --no-cache

up:
	@echo "🚀 Starting FastAPI with ${DB_TYPE}..."
	DB_TYPE=${DB_TYPE} docker compose up -d --build

down:
	@echo "🛑 Stopping and removing all containers..."
	docker compose down

logs:
	@echo "📜 Viewing logs..."
	docker compose logs -f

restart: down up
	@echo "🔄 Restarted FastAPI service!"

revision:
	@read -p "Enter revision message: " msg; \
	docker compose exec fastapi alembic revision --autogenerate -m "$$msg"

upgrade:
	@echo "📦 Upgrading database to latest revision..."
	docker compose exec fastapi alembic upgrade head

clean: down
	@echo "🧹 Cleaning up volumes..."
	docker volume rm postgres_data mysql_data || true

disable-postgres:
	@echo "🛑 Disabling PostgreSQL..."
	docker compose stop postgres
	docker compose rm -f postgres

disable-mysql:
	@echo "🛑 Disabling MySQL..."
	docker compose stop mysql
	docker compose rm -f mysql

disable-mongo:
	@echo "🛑 Disabling Mongo..."
	docker compose stop mongo
	docker compose rm -f mongo
