from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager

from models import Base

DB_URL = "sqlite+aiosqlite:///expenses.db"
engine = create_async_engine(DB_URL)

session_maker = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def create_async_session() -> AsyncGenerator[AsyncSession,]:
    async with session_maker() as session:
        try:
            print(f"Creating a session with DB")
            yield session
        finally:
            print(f"Closing DB session")
            await session.close()

async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
