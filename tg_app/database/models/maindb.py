from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self) -> None:
        self._engine = create_async_engine(
            "sqlite+aiosqlite:///tg_app/tgfood.sqlite", echo=True)
        self._session = sessionmaker(self._engine,
                                     expire_on_commit=False,
                                     class_=AsyncSession)()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._session, name)

    async def create_all(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async_db_session = AsyncDatabaseSession()
