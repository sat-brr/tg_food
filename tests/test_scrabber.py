import json
import os
from typing import List

import aiohttp
import pytest
from aioresponses import aioresponses
from bs4 import BeautifulSoup

from tg_app import scrabber


PEREHVAT1 = 'https://calorizator.ru/product/all'
PEREHVAT2 = 'https://calorizator.ru/product/all?page=1'
FIXTURES_PATH = os.path.abspath('tests/fixtures')
TEST_FIRST_PAGE = os.path.join(FIXTURES_PATH, 'first_page.html')
TEST_SECOND_PAGE = os.path.join(FIXTURES_PATH, 'second_page.html')
FIRST_PAGE_JSON = os.path.join(FIXTURES_PATH, 'first_page.json')
SECOND_PAGE_JSON = os.path.join(FIXTURES_PATH, 'second_page.json')
TEST_URL = 'http://tester123.br'
BAD_STATUS_CODE = [400, 404, 500, 502]


def get_html_page(path) -> str:
    with open(path, 'r') as file:
        return file.read()


def get_soup_page(path: str) -> BeautifulSoup:
    with open(path, 'r') as file:
        data = file.read()
        return BeautifulSoup(data, 'html.parser')


def read_json(path: str) -> List[dict]:
    with open(path, 'r') as file:
        return json.load(file)


@pytest.mark.asyncio
@pytest.mark.parametrize("status", BAD_STATUS_CODE)
async def test_bad_get_page_soup(status: int) -> None:
    session = aiohttp.ClientSession()
    with aioresponses() as mock:
        mock.get(TEST_URL, status=status)
        response = await scrabber.get_page_soup(session, TEST_URL)
        assert not response


@pytest.mark.asyncio
async def test_ok_get_page_soup() -> None:
    session = aiohttp.ClientSession()
    with aioresponses() as mock:
        mock.get(TEST_URL, status=200, body='Well Done!')
        response = await scrabber.get_page_soup(session, TEST_URL)
        assert response == BeautifulSoup('Well Done!', 'html.parser')


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_page, result_path",
    [(TEST_FIRST_PAGE, FIRST_PAGE_JSON), (TEST_SECOND_PAGE, SECOND_PAGE_JSON)]
)
async def test_collect_products_data(test_page: str, result_path: str) -> None:
    data = get_soup_page(test_page)
    expected_result = read_json(result_path)
    result = await scrabber.collect_products_data(data)
    assert result == expected_result


@pytest.mark.asyncio
async def test_write_data(monkeypatch: pytest.MonkeyPatch) -> None:
    data = read_json(FIRST_PAGE_JSON)

    async def mockreturn(*args, **kwargs) -> None:
        return

    monkeypatch.setattr(scrabber, 'write_data', mockreturn)
    result = await scrabber.write_data(data)
    assert not result


@pytest.mark.asyncio
async def test_start_scrabber(monkeypatch: pytest.MonkeyPatch) -> None:
    page1 = get_html_page(TEST_FIRST_PAGE)
    page2 = get_html_page(TEST_SECOND_PAGE)
    with aioresponses() as mock:

        async def mockreturn(*args, **kwargs) -> None:
            return

        monkeypatch.setattr(scrabber, 'write_data', mockreturn)
        mock.get(PEREHVAT1, status=200, body=page1)
        mock.get(PEREHVAT2, status=200, body=page2)
        result = await scrabber.parse_and_write()
        assert result
