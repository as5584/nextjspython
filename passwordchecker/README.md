# Password Strength Checker

Separated **backend** (FastAPI industrial layout) and **frontend** (Next.js).

## Structure

```
passwordchecker/
  backend/          # FastAPI: routers, schemas, services, repositories
  frontend/         # Next.js App Router UI
```

## Run backend

```bash
cd passwordchecker/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8004
```

API docs: http://127.0.0.1:8004/docs

## Run frontend

```bash
cd passwordchecker/frontend
npm install
npm run dev -- -p 3004
```

Open: http://localhost:3004

Frontend expects API at `NEXT_PUBLIC_API_URL` (see `frontend/.env.local`).
