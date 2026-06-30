"""Application entry point and FastAPI server configuration.
Initializes the FastAPI application, registers all routers for the layered
architecture (routers for domain entities), and manages the application
lifecycle including database table creation at startup.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.exc import IntegrityError
from core_app.core.config import settings
from core_app.database.session import create_tables
from core_app.routers import (
    category_router,
    transaction_type_router,
    item_router,
    user_router,
    transaction_router,
    currency_router,
    account_router,
    budget_router,
    auth_router
)

API_V1_PREFIX = "/api/v1"


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

app.include_router(auth_router.router, prefix=API_V1_PREFIX)
app.include_router(category_router.router, prefix=API_V1_PREFIX)
app.include_router(transaction_type_router.router, prefix=API_V1_PREFIX)
app.include_router(item_router.router, prefix=API_V1_PREFIX)
app.include_router(user_router.router, prefix=API_V1_PREFIX)
app.include_router(transaction_router.router, prefix=API_V1_PREFIX)
app.include_router(currency_router.router, prefix=API_V1_PREFIX)
app.include_router(account_router.router, prefix=API_V1_PREFIX)
app.include_router(budget_router.router, prefix=API_V1_PREFIX)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity violations globally.

    Converts unhandled SQLAlchemy IntegrityErrors (e.g. unique constraint
    violations) into clean 409 responses instead of exposing stack traces.

    Args:
        request: The incoming request.
        exc: The IntegrityError raised by SQLAlchemy.

    Returns:
        JSONResponse: 409 Conflict with a generic, safe message.
    """
    return JSONResponse(
        status_code=409,
        content={"detail": "Resource already exists or violates a uniqueness constraint."}
    )


@app.get("/")
def read_root():
    """Health check endpoint.

    Returns:
        dict: Status and current environment.
    """
    return {"status": "ok", "environment": settings.ENVIRONMENT}
