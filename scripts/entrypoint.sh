#!/bin/sh
set -e  

echo "⏳ Waiting for database..."
sleep 5

echo "📦 Running migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI app..."
exec gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 60
