from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import asyncio
from product_worker import get_product
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from users_crud import CheckUser
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import dotenv
import os
import time

dotenv.load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class CheckAuth(StatesGroup):
    phone_input = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    chk = CheckUser.check_on_user_id(message.from_user.id)
    if not chk:
        await message.reply('Введите Ваш номер телефона в формате 89997776655')
        await CheckAuth.phone_input.set()
    else:
        await message.answer("Для получения информации о продукте введите название продукта и" \
                             " через запятую количество грамм. Если не указывать граммы, выведется на 100г." \
                             " Пример: Морковь фиолетовая, 100")


@dp.message_handler(state=CheckAuth.phone_input)
async def process_check_phone(message: types.Message, state: FSMContext):
    usr_id = message.from_user.id
    await state.update_data(phone_input=int(message.text))
    data = await state.get_data()
    phone = int(data['phone_input'])
    response = CheckUser.check_on_phone(phone)

    if response:
        CheckUser.update(phone, {'user_id': usr_id})
        await message.answer("Для получения информации о продукте введите название продукта и" \
                             " через запятую количество грамм. Если не указывать граммы, выведется на 100г." \
                             " Пример: Морковь фиолетовая, 100")
    else:
        await message.answer('Block')
        return

    await state.finish()


@dp.message_handler(Text)
async def echo(message: types.Message):
    await message.answer('Пожалуйста, подождите...')
    mes = message.text.split(',')
    gram = 100
    if 1 < len(mes) < 3:
        try:
            gram = int(mes[1])
        except:
            await message.answer("Что то пошло не так. Будет выведена информация на 100г")
    if len(mes) > 2:
        await message.answer("Укажите одно число после запятой")
        return

    product_list = get_product(mes[0], gram)

    if product_list:

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


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
