import json
import os

import pytest

from tg_app import product_worker

FIXTURES_PATH = os.path.abspath('tests/fixtures')
TEST_PROD_LIST = os.path.join(FIXTURES_PATH, 'products_list.json')
TEST_FILTERED_PROD_LIST = os.path.join(FIXTURES_PATH,
                                       'filtered_products_list.json')
TEST_CALC_PROD_LIST = os.path.join(FIXTURES_PATH, 'calc_prod_list.json')


def get_product_list(path):
    with open(path, 'r') as file:
        return json.load(file)


def get_calc_prod_list(path):
    with open(path, 'r') as file:
        return json.load(file)


def get_filtered_products_list(path):
    with open(path, 'r') as file:
        return json.load(file)


async def ok_mockreturn(*args, **kwargs):
    return get_product_list(TEST_PROD_LIST)


async def not_found_mockreturn(*args, **kwargs) -> None:
    return


@pytest.mark.asyncio
@pytest.mark.parametrize('find_name', ['Морковь', 'Яблоко', '123'])
async def test_find_and_calc(monkeypatch: pytest.MonkeyPatch,
                             find_name: str) -> None:
    if find_name == 'Морковь':
        expected_result = (
            get_filtered_products_list(TEST_FILTERED_PROD_LIST),
            100
            )

        monkeypatch.setattr(product_worker,
                            'find_similar_products', ok_mockreturn)
    else:
        expected_result = None
        monkeypatch.setattr(product_worker,
                            'find_similar_products', not_found_mockreturn)
    result = await product_worker.find_and_calc(find_name)

    assert result == expected_result


@pytest.mark.asyncio
async def test_get_calc_stats() -> None:
    products_list = get_filtered_products_list(TEST_FILTERED_PROD_LIST)
    expected_result = get_calc_prod_list(TEST_CALC_PROD_LIST)
    result = []
    for product in products_list:
        res = await product_worker.calc_stats(product, 150)
        result.append(res)

    assert result == expected_result
