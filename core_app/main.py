from fastapi import FastAPI
from contextlib import asynccontextmanager
from core_app.core.config import settings
from core_app.database.session import create_tables
from core_app.routers import (
    item_type_router,
    transaction_type_router,
    item_router,
    user_router,
    transaction_router,
    currency_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(
    title="A1 Backend Core",
    description="Personal Finance & Investment API",
    version="0.2.0",
    lifespan=lifespan
)

app.include_router(item_type_router.router)
app.include_router(transaction_type_router.router)
app.include_router(item_router.router)
app.include_router(user_router.router)
app.include_router(transaction_router.router)
app.include_router(currency_router.router)
@app.get("/")
def read_root():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
