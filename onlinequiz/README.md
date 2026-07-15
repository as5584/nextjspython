# Online Quiz

Separated **backend** (FastAPI industrial layout) and **frontend** (Next.js).

## Structure

```
onlinequiz/
  backend/          # FastAPI: routers, schemas, services, repositories
  frontend/         # Next.js App Router UI
```

## Run backend

```bash
cd onlinequiz/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8005
```

API docs: http://127.0.0.1:8005/docs

## Run frontend

```bash
cd onlinequiz/frontend
npm install
npm run dev -- -p 3005
```

Open: http://localhost:3005

Frontend expects API at `NEXT_PUBLIC_API_URL` (see `frontend/.env.local`).
