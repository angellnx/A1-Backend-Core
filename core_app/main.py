from fastapi import FastAPI
from core_app.core.config import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT
    }
