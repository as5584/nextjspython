from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import books_router, issues_router, reports_router

app = FastAPI(title="Library Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router)
app.include_router(issues_router)
app.include_router(reports_router)


@app.get("/")
def root():
    return {"message": "Library Management System API", "docs": "/docs"}