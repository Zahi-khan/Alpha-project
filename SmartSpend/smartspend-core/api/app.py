from fastapi import FastAPI

from api.routes import router
from api.sessions import router as sessions_router

app = FastAPI(
    title="SmartSpend API",
    version="1.0.0"
)

app.include_router(router)
app.include_router(sessions_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to SmartSpend API",
        "status": "running"
    }
