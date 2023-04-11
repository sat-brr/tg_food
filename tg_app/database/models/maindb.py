import os

import dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()
TEST = os.getenv("TEST") == 'True'
DB_NAME = os.getenv("TEST_DB_NAME") if TEST else os.getenv("DB_NAME")
DB_URL = f"sqlite+aiosqlite:///{DB_NAME}"

Base = declarative_base()
engine = create_async_engine(
            DB_URL, echo=True)
async_db_session = sessionmaker(engine,
                                expire_on_commit=False,
                                class_=AsyncSession)()


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
