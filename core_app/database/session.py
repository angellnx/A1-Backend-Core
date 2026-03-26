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
    Base.metadata.create_all(bind=engine)

def get_session(): 
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close() 
