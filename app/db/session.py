import os
from typing import Generator, AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Load environment variables from .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# --- ASYNCHRONOUS SETUP (for the new FastAPI API) ---

# 1. Async Database URL (uses asyncpg)
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
if not ASYNC_DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env file for async connection")

# 2. Async Engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    future=True
)

# 3. Async Session Maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an asynchronous database session.
    This is used by the API controllers.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# --- SYNCHRONOUS SETUP (for the old, deprecated CLI) ---

# 1. Sync Database URL (uses psycopg2, which you already have from Phase 2)
SYNC_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
if not SYNC_DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env file for sync connection")

# 2. Sync Engine
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=False,
    future=True
)

# 3. Sync Session Maker - This is the 'SessionLocal' that console.py needs!
SessionLocal = sessionmaker(
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
    future=True
)
