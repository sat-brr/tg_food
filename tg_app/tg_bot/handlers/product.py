from tg_app.tg_bot.bot_config import dp
from aiogram import Dispatcher, types
from tg_app.product_worker import get_product
from aiogram.utils.markdown import hbold, hlink
import time
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

class ProdName(StatesGroup):
    product_name = State()


async def get_product_name(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('/back')
    await message.answer("Для получения информации о продукте введите название продукта и" \
                            " через запятую количество грамм. Если не указывать граммы, выведется на 100г." \
                            " Пример: Морковь фиолетовая, 100", reply_markup=keyboard)
    await ProdName.product_name.set()


async def get_products(message: types.Message, state: FSMContext) -> None:
    await state.update_data(product_name=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('/back')
    mes = message.text.split(',')
    gram = 100
    await message.answer('Пожалуйста, подождите...', reply_markup=keyboard)

    if 1 < len(mes) < 3:
        try:
            gram = int(mes[1])
        except Exception:
            await message.answer("Что то пошло не так. Будет выведена информация на 100г")

    if len(mes) > 2:
        await message.answer("Укажите одно число после запятой")
        return

    if product_list := get_product(mes[0].strip(), gram):
        for index, prod in enumerate(product_list):

            card = f'{hlink(prod.get("name"), prod.get("url"))}\n' \
                f'{hbold("Информация на ")}{gram} грамм.\n' \
                f'{hbold("Белок: ")}{prod["protein"]}\n' \
                f'{hbold("Жиры: ")}{prod["fat"]}\n' \
                f'{hbold("Углеводы: ")}{prod["carbohydrate"]}\n' \
                f'{hbold("Ккал: ")}{prod["kcal"]}\n'

            if index%10 == 0:
                time.sleep(5)

            await message.answer(card)
    else:
        await message.answer("Ничего не найдено.")


def register_handler(dp: Dispatcher) -> None:
    dp.register_message_handler(get_product_name, Text(equals='Поиск Продуктов'))
    dp.register_message_handler(get_products, state=ProdName.product_name)
