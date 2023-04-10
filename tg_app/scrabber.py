import asyncio
from random import randint
from typing import Literal

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from tg_app.database.models.products import Product

HEADERS = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
FIRST_PAGE = 'https://calorizator.ru/product/all'
PAGES_LINK = 'https://calorizator.ru/product/all?page='


async def write_data(products_list: list[dict]) -> None:
    for product_data in products_list:
        check_res = await Product.check_by_name(product_data['name'])
        if not check_res:
            await Product.create(**product_data)


async def collect_products_data(page_data: BeautifulSoup) -> list[dict]:
    table = page_data.find('table')
    data_tbody = table.find('tbody').find_all('tr')

    products_data = []

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

        products_data.append(product)
    return products_data


async def get_products_list(pages_soup: list[BeautifulSoup]) -> list[dict]:
    product_list = []
    for soup in pages_soup:
        if soup:
            product_list.extend(await collect_products_data(soup))

    return product_list


async def get_page_soup(
        session: ClientSession,
        url: str,
        try_connect: int = 0
        ) -> BeautifulSoup | None:

    try:
        await asyncio.sleep(randint(3, 7))
        response = await session.get(url=url, headers=HEADERS)
        response.raise_for_status()

        return BeautifulSoup(await response.text(), 'html.parser')

    except Exception as err:
        print(f'Connection error. {err}\n Try again...')
        while try_connect < 3:
            await asyncio.sleep(randint(3, 7))
            return await get_page_soup(session, url, try_connect + 1)


async def collect_all_pages_soup(
        session: ClientSession,
        urls_list: list[str]
        ) -> list[BeautifulSoup]:

    pages_soup = []

    for url in urls_list:
        response = await get_page_soup(session, url)
        if response:
            pages_soup.append(response)

    return pages_soup


async def get_main_page_soup_and_count_pages(
        session: ClientSession
        ) -> tuple[BeautifulSoup, int] | None:

    main_page_soup = await get_page_soup(session, FIRST_PAGE)

    if not main_page_soup:
        return

    last_page_num = int(
            main_page_soup.find('div', class_='item-list')
            .find('li', class_='pager-last').text
            )

    return main_page_soup, last_page_num


async def create_pages_urls(number_of_pages: int) -> list[str]:
    urls_list = []

    for num in range(1, number_of_pages):
        url = f"{PAGES_LINK}{num}"
        urls_list.append(url)

    return urls_list


async def parse_and_write() -> Literal[True] | None:
    async with ClientSession() as session:
        first_page = await get_main_page_soup_and_count_pages(session)

        if not first_page:
            return

        first_page_soup, number_of_pages = first_page
        urls_list = await create_pages_urls(number_of_pages)

        pages_soup = await collect_all_pages_soup(session, urls_list)
        pages_soup.insert(0, first_page_soup)

    products_list = await get_products_list(pages_soup)

    await write_data(products_list)

    return True
