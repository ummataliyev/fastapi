# FastAPI Template

Beginner-friendly FastAPI template with a clean layered architecture:
`router -> service -> repository -> database`.

## What You Get
- Async FastAPI + SQLAlchemy setup.
- User CRUD example (`/users`).
- Alembic migrations for PostgreSQL.
- Optional Redis, MongoDB, and AWS helper modules.
- Standard API response shape:
  - `status`
  - `message`
  - `data`
- Starter unit and integration-style tests.

## Project Structure
```text
src/
  main.py                 # App entrypoint and global middleware/handlers
  routers/                # API endpoints
  services/               # Business logic
  repositories/           # Data access layer
  models/                 # SQLAlchemy models
  schemas/                # Pydantic request/response schemas
  response/               # Unified API response builders
  tests/                  # Unit + integration-style tests
db/
  storage/postgres/       # PostgreSQL engine/session
  storage/mysql/          # Optional MySQL engine/session
  storage/mongo/          # Optional Mongo client
  redis/                  # Optional Redis client
```

## Prerequisites
- Python 3.11+ (or Docker)
- PostgreSQL (for local non-Docker runs)

## Local Development
1. Create and activate a virtual environment.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy environment file and adjust values:
```bash
cp .env.dist .env
```
4. For local Postgres, set:
```env
DB_HOST=127.0.0.1
DB_PORT=5432
```
5. Run migrations:
```bash
alembic upgrade head
```
6. Start the app:
```bash
uvicorn src.main:app --reload --port 8000
```

Docs:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Docker Development
Start:
```bash
make up
```

Stop:
```bash
make down
```

Logs:
```bash
make logs
```

## User API Quickstart
Base path: `/users`

- `GET /users/{id}`: returns `200` or `404`
- `GET /users/`: returns `200`
- `POST /users/`: returns `201`, `409` (duplicate email), or `500`
- `PATCH /users/{id}`: returns `200`, `404`, `409`, or `500`
- `DELETE /users/{id}`: returns `200`, `404`, or `500`

Example create request:
```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```

## Environment Variables
Main DB:
- `DB_USER`
- `DB_NAME`
- `DB_HOST`
- `DB_PORT`
- `DB_PASSWORD`

Optional toggles:
- `REDIS_IS_ENABLE` (note: singular `ENABLE`)
- `MONGO_IS_ENABLED`
- `AWS_IS_ENABLE`

Optional tuning:
- `SQL_ECHO`
- `LIMIT_GET`
- `LIMIT_PPD`
- `TIME_GET`
- `TIME_PPD`

## Run Tests
```bash
pytest -q
```

If test collection fails with missing modules, install dependencies first:
```bash
pip install -r requirements.txt
```

## Notes for Beginners
- Put HTTP concerns in `routers/`.
- Put business rules in `services/`.
- Put database queries in `repositories/`.
- Keep schemas in `schemas/` and response formatting in `response/`.
