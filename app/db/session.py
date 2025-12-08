# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Use DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env file")

# Create engine with connection pooling and echo for debugging
engine = create_engine(
    DATABASE_URL,
    echo=False,           # Set True only during development
    pool_pre_ping=True,   # Prevents connection issues
    future=True
)

# Session factory — this is what we'll inject
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=Session,
    future=True
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that yields a database session.
    Usage in services: db: Session = next(get_db())
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()