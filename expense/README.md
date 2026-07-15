# Expense Tracker

Separated **backend** (FastAPI industrial layout) and **frontend** (Next.js).

## Structure

```
expense/
  backend/          # FastAPI: routers, schemas, services, repositories
  frontend/         # Next.js App Router UI
```

## Run backend

```bash
cd expense/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

API docs: http://127.0.0.1:8002/docs

## Run frontend

```bash
cd expense/frontend
npm install
npm run dev -- -p 3002
```

Open: http://localhost:3002

Frontend expects API at `NEXT_PUBLIC_API_URL` (see `frontend/.env.local`).
