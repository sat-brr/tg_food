import asyncio

from tg_app.database.models.maindb import create_db
from tg_app.database.models.products import Product  # noqa: F401
from tg_app.database.models.users import User  # noqa: F401


async def init_base() -> None:
    await create_db()


async def start() -> None:
    await init_base()


if __name__ == '__main__':
    asyncio.run(start())
