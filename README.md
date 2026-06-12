# Habit Tracker

Personal habit tracker with daily check-ins, streak tracking, and completion stats.

## Stack

- **Backend** — FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, PyJWT
- **Frontend** — React, Vite, Tailwind CSS *(in progress)*
- **Infra** — Docker (local Postgres), Railway (backend), Vercel (frontend)

## Getting started

### Prerequisites

- Python 3.12+
- Docker
- Node 18+

### Backend

```bash
cd backend
docker-compose up -d          # start Postgres
cp .env.example .env          # fill in SECRET_KEY
pip install -e ".[dev]"
alembic upgrade head
uvicorn backend.main:app --reload
```

API is available at `http://localhost:8000`. Interactive docs at `/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App is available at `http://localhost:5173`.

## API

All endpoints except `/health`, `/auth/register`, and `/auth/login` require a Bearer token.

### Auth

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register` | Create account |
| `POST` | `/auth/login` | Returns JWT |
| `GET` | `/auth/me` | Current user |

### Habits

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/habits/` | Create habit |
| `GET` | `/habits/` | List habits |
| `GET` | `/habits/{id}` | Get habit |
| `PUT` | `/habits/{id}` | Update habit |
| `DELETE` | `/habits/{id}` | Delete habit |
| `GET` | `/habits/{id}/streak` | Current streak (days) |
| `GET` | `/habits/{id}/logs` | List completions |
| `POST` | `/habits/{id}/logs` | Check in for a date |
| `DELETE` | `/habits/{id}/logs/{completion_id}` | Remove check-in |

### Stats

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/stats/streaks` | All habits with current streak |
| `GET` | `/stats/summary?days=7` | Completions, missed, longest streak over N days |

## Running tests

```bash
cd backend
pytest                    # all tests
pytest -m stats           # stats tests only
pytest -m streaks         # streak unit tests only
pytest -m auth            # auth tests only
pytest -m focus           # current working test
```

## Linting

```bash
ruff check . --fix
black .
```
