# Cas Commerce ERP

Een volledig FastAPI + React ERP/CRM-platform voor e-commerce organisaties. Deze repository bevat zowel de backend API (`api/`) als de moderne frontend (`web/`).

## Project structuur

```
/api/app
  core/         # Configuratie, database en security
  models/       # SQLAlchemy modellen
  routers/      # FastAPI routers per domein
  schemas/      # Pydantic-schema's
  services/     # Domeinlogica (inventory, finance, integrations)
  tests/        # Pytest suites
/web            # React + Vite frontend
```

## Backend quickstart

```bash
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

De applicatie maakt standaard gebruik van SQLite (`erp.db`). Pas `DATABASE_URL` aan in `.env` voor PostgreSQL.

## Tests

```bash
cd api
pytest
```

## Frontend quickstart

```bash
cd web
npm install
npm run dev
```

De frontend communiceert met de API via `http://localhost:8000` (configureerbaar).

## Docker

Gebruik `docker-compose up` om API, frontend en database gezamenlijk te starten.
