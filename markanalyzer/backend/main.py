from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import API_TITLE, API_VERSION
from routers import marks_router

app = FastAPI(title=API_TITLE, version=API_VERSION, redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(marks_router)


@app.get("/")
def root():
    return {"message": API_TITLE + " API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
