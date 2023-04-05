import asyncio

from bot_config import dp

from tg_app.tg_bot.handlers import auth, common, product


async def main() -> None:
    common.register_handler(dp)
    auth.register_handler(dp)
    product.register_handler(dp)
    await dp.start_polling(dp)


if __name__ == '__main__':
    asyncio.run(main())
