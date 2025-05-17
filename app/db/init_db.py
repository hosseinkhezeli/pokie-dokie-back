from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base
from app.db.session import engine

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 