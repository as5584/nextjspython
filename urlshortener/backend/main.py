from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import API_TITLE, API_VERSION
from routers import urls_router

# redirect_slashes=False avoids 307/308 that break browser fetch via proxy
app = FastAPI(title=API_TITLE, version=API_VERSION, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(urls_router)


@app.get("/")
def root():
    return {"message": f"{API_TITLE} API", "docs": "/docs", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}
