import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from tg_app.database.models.users import User
from tg_app.tg_bot.bot_config import dp


class RegUsr(StatesGroup):
    usr_phone = State()


async def get_phone_num(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('/back')
    await message.answer(
        "Введите свой номер телефона в формате '89997776655'"
        " или команду /back для отмены.",
        reply_markup=keyboard
        )
    await RegUsr.usr_phone.set()


async def process_check_phone(message: types.Message,
                              state: FSMContext) -> None:
    usr_id = message.from_user.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('/back')
    await state.update_data(phone_input=message.text)
    data = await state.get_data()
    phone = data['phone_input']
    res = re.search(r"^[0-9]+$", phone)
    if res is None or 11 < res.span()[1] > 11 or phone[0] != '8':
        await message.answer("Неверно указан номер. Повторите попытку"
                             " или введите команду /back для отмены.",
                             reply_markup=keyboard)
        return
    if not await User.check_by_phone(phone):
        await User.create(user_id=usr_id, user_phone=int(phone))
    await message.answer("Вы зарегистрированы."
                         " Введите команду /back для продолжения.",
                         reply_markup=keyboard)


def register_handler(dp: dp) -> None:
    dp.register_message_handler(get_phone_num, commands='register')
    dp.register_message_handler(process_check_phone, state=RegUsr.usr_phone)
