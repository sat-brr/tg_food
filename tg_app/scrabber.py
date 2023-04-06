import asyncio
import json
import time
from random import randint

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from tg_app.database.models.products import Product

start_time = time.time()

HEADERS = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
MAIN_PAGE = 'https://calorizator.ru/product/all'
PAGES_LINK = 'https://calorizator.ru/product/all?page='
PATH_TO_FILE = 'tg_app/products.json'


async def write_data(products_list: list[dict]) -> None:
    for product_data in products_list:
        check_res = await Product.check_by_name(product_data['name'])
        if not check_res:
            await Product.create(**product_data)

    with open(PATH_TO_FILE, 'w') as file:
        file.write(json.dumps(products_list, indent=4, ensure_ascii=False))


async def collect_data(page_data: BeautifulSoup) -> dict:
    table = page_data.find('table')
    data_tbody = table.find('tbody').find_all('tr')

    products_list = []

    for dtr in data_tbody:
        name = (
            dtr.find('td',
                     class_='views-field views-field-title active')
            .text.strip()
            )

        url = (
            dtr.find('td',
                     class_='views-field views-field-title active')
            .find('a').get('href')
            )

        protein = (
            dtr.find('td',
                     class_='views-field views-field-field-protein-value')
            .text.strip()
            )

        fat = (
            dtr.find('td',
                     class_='views-field views-field-field-fat-value')
            .text.strip()
            )

        carbohydrate = (
            dtr.find('td',
                     class_='views-field views-field-field-carbohydrate-value')
            .text.strip()
            )

        kcal = (
            dtr.find('td',
                     class_='views-field views-field-field-kcal-value')
            .text.strip()
            )

        product = {
            'name': name,
            'protein': protein,
            'fat': fat,
            'carbohydrate': carbohydrate,
            'kcal': kcal,
            'url': f'https://calorizator.ru{url}',
        }

        products_list.append(product)
    return products_list


async def get_page_data(session, url, try_connect=0) -> BeautifulSoup | None:
    try:
        await asyncio.sleep(randint(3, 7))
        response = await session.get(url=url, headers=HEADERS)
        response.raise_for_status()

        return BeautifulSoup(await response.text(), 'html.parser')

    except Exception as err:
        print(f'Connection error. {err}\n Try again...')
        while try_connect < 3:
            await asyncio.sleep(randint(3, 7))
            return await get_page_data(session, url, try_connect + 1)


async def main() -> None:
    async with ClientSession() as session:
        main_page = await get_page_data(session, MAIN_PAGE)

        if not main_page:
            return

        number_of_pages = int(
            main_page.find('div', class_='item-list')
            .find('li', class_='pager-last').text
            )

        urls_list = []
        urls_list.extend(f"{PAGES_LINK}{num}"
                         for num in range(1, number_of_pages))

        tasks = []
        for url in urls_list:
            task = asyncio.create_task(get_page_data(session, url))
            tasks.append(task)

        pages_data = await asyncio.gather(*tasks)
        pages_data.insert(0, main_page)

        products_list = []

        for page_data in pages_data:
            if page_data:
                products_list.extend(await collect_data(page_data))
            else:
                continue

        await write_data(products_list)

        return True
