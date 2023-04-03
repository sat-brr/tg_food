from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from tg_app.tg_bot.bot_config import dp
from tg_app.database.models.users import CheckUser, CrudUser
import re


class RegUsr(StatesGroup):
    usr_phone = State()


async def get_phone_num(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add('/back')
    await message.answer("Введите свой номер телефона в формате '89990018022' или команду /back для отмены.",
                        reply_markup=keyboard)
    await RegUsr.usr_phone.set()


async def process_check_phone(message: types.Message, state: FSMContext) -> None:
    usr_id = message.from_user.id
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add('/back')
    await state.update_data(phone_input=int(message.text))
    data = await state.get_data()
    phone = data['phone_input']
    res = re.search(r"^[0-9]+$")
    if res is None or 11 < res.span()[1] > 11 or phone[0] != '8':
        await message.answer("Неверно указан номер. Повторите попытку или введите команду /back для отмены.", reply_markup=keyboard)
        return
    if not CheckUser().check_by_phone(phone):
        CrudUser().create_user(usr_id, int(phone))
    await message.answer("Вы зарегистрированы. Введите команду /back для продолжения.", reply_markup=keyboard)


def register_handler(dp: Dispatcher) -> None:
    dp.register_message_handler(get_phone_num, commands='register')
    dp.register_message_handler(process_check_phone, state=RegUsr.usr_phone)
