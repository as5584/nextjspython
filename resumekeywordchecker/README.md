# Resume Keyword Checker

Separated **backend** (FastAPI industrial layout) and **frontend** (Next.js).

## Structure

```
resumekeywordchecker/
  backend/          # FastAPI: routers, schemas, services, repositories
  frontend/         # Next.js App Router UI
```

## Run backend

```bash
cd resumekeywordchecker/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8010
```

API docs: http://127.0.0.1:8010/docs

## Run frontend

```bash
cd resumekeywordchecker/frontend
npm install
npm run dev -- -p 3010
```

Open: http://localhost:3010

Frontend expects API at `NEXT_PUBLIC_API_URL` (see `frontend/.env.local`).
