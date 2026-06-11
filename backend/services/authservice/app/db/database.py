from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import settings

async_engine = create_async_engine(
    url=settings.get_database_url,
    poolclass=NullPool
)

SessionLocal = async_sessionmaker(bind=async_engine, autoflush=False)

class Base(DeclarativeBase):
    pass

async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()