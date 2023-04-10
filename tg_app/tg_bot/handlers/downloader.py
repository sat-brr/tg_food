from aiogram import types
from tg_app.tg_bot.bot_config import dp
from tg_app.database.models.users import User
from tg_app import scrabber
import time


async def download_products(message: types.Message) -> None:
    usr_id = message.from_user.id
    comnds = ['Поиск Продуктов']
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(*comnds)

    if User.get_by_tg_id(usr_id).admin:
        await message.answer('Подождите, обновляю данные...')
        st = time.time()
        await scrabber.main()
        ft = time.time() - st
        await message.answer(f'Данные обновлены. Время выполнения: {ft}',
                             reply_markup=keyboard)
    else:
        await message.answer('Нет прав для выполнения этой операции.',
                             reply_markup=keyboard)


def register_handler(dp: dp) -> None:
    dp.register_message_handler(download_products, commands=['update'])
