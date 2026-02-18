# FastAPI Template

Beginner-friendly FastAPI starter project with a layered architecture:
`router -> service -> repository -> database`.

## Features
- User CRUD example (`/users`).
- Async FastAPI + SQLAlchemy.
- PostgreSQL support (default).
- Optional Redis and Mongo helpers.
- Alembic migrations.
- Unit + integration-style tests.

## Project Structure
```text
src/
  main.py                 # FastAPI app entrypoint
  routers/                # API routes
  services/               # Business logic
  repositories/           # Data access
  models/                 # SQLAlchemy models
  schemas/                # Pydantic schemas
  response/               # Standardized API response builders
  tests/                  # Unit + integration tests
db/
  storage/postgres/       # PostgreSQL engine/session setup
  redis/                  # Redis connection helper
```

## Prerequisites
- Python 3.11+ (or Docker).
- PostgreSQL (if running locally without Docker).

## Local Setup (without Docker)
1. Create and activate a virtual environment.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create `.env` from `.env.dist` and fill required values.
4. Run migrations:
```bash
alembic upgrade head
```
5. Start the app:
```bash
uvicorn src.main:app --reload --port 8000
```

Open docs at: `http://127.0.0.1:8000/docs`

## Docker Setup
```bash
make up
```

Stop services:
```bash
make down
```

## Run Tests
```bash
pytest -q
```

## Notes for Beginners
- Keep business rules in `services/`, not in `routers/`.
- Keep raw DB access in `repositories/`.
- Keep request/response validation in `schemas/` and `response/`.
