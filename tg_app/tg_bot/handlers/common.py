from aiogram import types
from aiogram.dispatcher import FSMContext

from tg_app.database.models.users import User
from tg_app.tg_bot.bot_config import dp


async def start(message: types.Message) -> None:
    if User.get_by_tg_id(message.from_user.id):
        comnds = ['Поиск Продуктов']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*comnds)
        await message.answer('Добро пожаловать. Выберите категорию',
                             reply_markup=keyboard)

    else:
        await message.reply(
            "Для продолжения требуется регистрация."
            " Введите команду /register для перехода к регистрации."
            )


async def back(message: types.Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Поиск Продуктов')
    await state.finish()
    if User.get_by_tg_id(message.from_user.id):
        await message.answer('Выберите категорию', reply_markup=keyboard)
    else:
        await message.answer('Введите команду /start',
                             reply_markup=types.ReplyKeyboardRemove())


def register_handler(dp: dp) -> None:
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(back, commands='back', state="*")
