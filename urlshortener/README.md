# URL Shortener

Separated **backend** (FastAPI industrial layout) and **frontend** (Next.js).

## Structure

```
urlshortener/
  backend/          # FastAPI: routers, schemas, services, repositories
  frontend/         # Next.js App Router UI
```

## Run backend

```bash
cd urlshortener/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8003
```

API docs: http://127.0.0.1:8003/docs

## Run frontend

```bash
cd urlshortener/frontend
npm install
npm run dev -- -p 3003
```

Open: http://localhost:3003

Frontend expects API at `NEXT_PUBLIC_API_URL` (see `frontend/.env.local`).
