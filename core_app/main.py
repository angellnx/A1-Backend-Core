from fastapi import FastAPI
from core_app.core.config import settings
from core_app.routers import (
    item_type_router,
    transaction_type_router,
    item_router,
    user_router,
    transaction_router
)

app = FastAPI(
    title="A1 Backend Core",
    description="Personal finance and investment management API",
    version="0.1.0"
)

app.include_router(item_type_router.router)
app.include_router(transaction_type_router.router)
app.include_router(item_router.router)
app.include_router(user_router.router)
app.include_router(transaction_router.router)

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT
    }
