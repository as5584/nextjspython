# Attendance Manager

Separated **backend** (FastAPI industrial layout) and **frontend** (Next.js).

## Structure

```
attendance/
  backend/          # FastAPI: routers, schemas, services, repositories
  frontend/         # Next.js App Router UI
```

## Run backend

```bash
cd attendance/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

API docs: http://127.0.0.1:8001/docs

## Run frontend

```bash
cd attendance/frontend
npm install
npm run dev -- -p 3001
```

Open: http://localhost:3001

Frontend expects API at `NEXT_PUBLIC_API_URL` (see `frontend/.env.local`).
