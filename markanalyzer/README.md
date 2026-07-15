# Marks Analyzer

Separated **backend** (FastAPI industrial layout) and **frontend** (Next.js).

## Structure

```
markanalyzer/
  backend/          # FastAPI: routers, schemas, services, repositories
  frontend/         # Next.js App Router UI
```

## Run backend

```bash
cd markanalyzer/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8006
```

API docs: http://127.0.0.1:8006/docs

## Run frontend

```bash
cd markanalyzer/frontend
npm install
npm run dev -- -p 3006
```

Open: http://localhost:3006

Frontend expects API at `NEXT_PUBLIC_API_URL` (see `frontend/.env.local`).
