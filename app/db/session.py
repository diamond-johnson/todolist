from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env file")

# Create engine with connection pooling and echo for debugging
engine = create_engine(
    DATABASE_URL,
    echo=False,           # Set True only during development
    pool_pre_ping=True,   # Prevents connection issues
    future=True
)


SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=Session,
    future=True
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that yields a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


