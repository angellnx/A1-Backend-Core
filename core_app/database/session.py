"""Database session management and initialization.

Handles SQLite database connection setup, session factory creation,
and provides a FastAPI dependency for obtaining database sessions.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

DATABASE_URL = "sqlite:///./a1.db"

engine = create_engine( 
    DATABASE_URL, 
    connect_args={"check_same_thread": False} 
)

SessionLocal = sessionmaker( 
    autocommit=False, 
    autoflush=False, 
    bind=engine 
)

def create_tables():
    """Create all database tables defined in Base metadata."""
    Base.metadata.create_all(bind=engine)

def get_session():
    """FastAPI dependency providing a database session per request."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close() 
