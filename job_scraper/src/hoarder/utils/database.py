from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker
from src.hoarder.utils.settings import settings
from typing import AsyncGenerator


def get_session() -> Session:
    """Get a database session"""
    engine = create_engine(settings.db_url, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_engine = create_async_engine(settings.db_url, echo=True)
    async_session = async_sessionmaker(async_engine, class_=AsyncSession)

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
