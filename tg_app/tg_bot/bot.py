import asyncio
from tg_app.tg_bot.handlers import auth, product, common
from bot_config import dp


async def main() -> None:
    common.register_handler(dp)
    auth.register_handler(dp)
    product.register_handler(dp)
    await dp.start_polling(dp)


if __name__ == '__main__':
    asyncio.run(main())