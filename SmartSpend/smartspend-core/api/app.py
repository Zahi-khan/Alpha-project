import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from api.sessions import router as sessions_router

app = FastAPI(
    title="SmartSpend API",
    version="1.0.0"
)

allowed_origins = [origin.strip() for origin in os.getenv(
    "SMARTSPEND_ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(sessions_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to SmartSpend API",
        "status": "running"
    }
