# Next.js + Python Mini Projects

Each tool has a **separate industrial FastAPI backend** and a **Next.js frontend**.

Frontends call the API through a **same-origin `/backend` proxy** (see each `frontend/next.config.mjs`).  
That avoids browser CORS issues and the common **Failed to fetch** error.

## Ports

| Project | Backend | Frontend |
|---------|---------|----------|
| attendance | 8001 | 3001 |
| expense | 8002 | 3002 |
| urlshortener | 8003 | 3003 |
| passwordchecker | 8004 | 3004 |
| onlinequiz | 8005 | 3005 |
| markanalyzer | 8006 | 3006 |
| duplicatefilefinder | 8007 | 3007 |
| folderorganizer | 8008 | 3008 |
| bulkfilerename | 8009 | 3009 |
| resumekeywordchecker | 8010 | 3010 |
| librarymanger | 8011 | 3011 |

## Important: run backend + frontend together

**Failed to fetch** almost always means the backend is not running.

### Helper script

```powershell
cd "C:\Users\ARUN VARSHAN SDR\OneDrive\Desktop\nextjspython"
.\run_project.ps1 -Project passwordchecker
```

### Manual example (password checker)

```powershell
# Terminal 1 — API
cd passwordchecker\backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8004

# Terminal 2 — UI
cd passwordchecker\frontend
npm install
npm run dev -- -p 3004
```

Open: http://localhost:3004  
API docs: http://127.0.0.1:8004/docs

For `librarymanger`, backend files are at the project root (not under `backend/`).

## After changing `.env.local` or `next.config.mjs`

Stop the frontend (Ctrl+C) and start it again so Next.js reloads the proxy config.

## Backend layout (industrial)

```
backend/
  main.py
  config.py
  routers/
  schemas/
  services/
  repositories/
  data/
```
