import os

import dotenv
from sqlalchemy.ext.asyncio import create_async_engine

from tg_app.database.models.maindb import Base

dotenv.load_dotenv()
dotenv_file = dotenv.find_dotenv()
dotenv.set_key(dotenv_file, 'TEST', 'True')
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_URL = f"sqlite+aiosqlite:///{TEST_DB_NAME}"


async def create_db():
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
