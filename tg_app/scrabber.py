from typing import Any, List
from bs4 import BeautifulSoup as bs
import json
import time
import asyncio
from aiohttp import ClientSession


start_time = time.time()

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
main_page = 'https://calorizator.ru/product/all'
pages_link = 'https://calorizator.ru/product/all?page='
path_to_file = 'tg_app/products.json'


async def collect_data(dtr: str) -> dict:
    name = dtr.find('td', class_='views-field views-field-title active').text.strip()
    url = dtr.find('td', class_='views-field views-field-title active').find('a').get('href')
    protein = dtr.find('td', class_='views-field views-field-field-protein-value').text.strip()
    fat = dtr.find('td', class_='views-field views-field-field-fat-value').text.strip()
    carbohydrate = dtr.find('td', class_='views-field views-field-field-carbohydrate-value').text.strip()
    kcal = dtr.find('td', class_='views-field views-field-field-kcal-value').text.strip()

    return {
        'name': name,
        'protein': protein,
        'fat': fat,
        'carbohydrate': carbohydrate,
        'kcal': kcal,
        'url': f'https://calorizator.ru{url}',
    }


async def get_dom(session: ClientSession, url: str) -> Any | None:

    try:
        await asyncio.sleep(2)
        response = await session.get(url, headers=headers)
        page_data = bs(await response.text(), 'html.parser')

        if page_data is None:
            print(f"None with page {url}")
        table = page_data.find('table')
        data_tbody = table.find('tbody').find_all('tr')
        tasks = []

        for dtr in data_tbody:
            task = asyncio.create_task(collect_data(dtr))
            tasks.append(task)

        return await asyncio.gather(*tasks)
    except Exception as err:
        print(f'Error with page {url}')


async def get_pages() -> None:
    async with ClientSession() as session:

        response = await session.get(url=main_page, headers=headers)

        first_page = bs(await response.text(), 'html.parser')

        pages_count = int(first_page.find('div', class_='item-list').find('li', class_='pager-last').text)

        urls_list = [main_page]

        for page in range(1, pages_count):
            url = f'{pages_link}{page}'
            urls_list.append(url)

        tasks = []
        
        for url in urls_list:
            task = asyncio.create_task(get_dom(session, url))
            tasks.append(task)
        
        pages_data = await asyncio.gather(*tasks)
        new_list = []

        for page in pages_data:
            new_list.extend(page)      

        with open('tg_app/products.json', 'w') as file:
            file.write(json.dumps(new_list, indent=4, ensure_ascii=False))


async def main() -> None:
    await(get_pages())
