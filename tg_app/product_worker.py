import json
from typing import List


def get_calc_stats(product: dict, gramm: int) -> dict:
    stats = ['protein', 'fat', 'carbohydrate', 'kcal']
    new_prod = product
    res = gramm / 100
    for stat in stats:
        new_prod[stat] = round(float(product[stat]) * res, 3)
    return new_prod


def get_filtering(product: dict, name: str, gramm: int) -> dict | None:
    name_words = name.split()
    product_name = product['name']
    product_nwords = product_name.split()
    len_name_words = len(name_words)
    len_prod_words = len(product_nwords)

    if product_nwords[0].lower() != name_words[0].lower():
        return

    if len_prod_words < len_name_words:
        return

    counter = sum(word in product_nwords for word in name_words)
    sov = counter/len_prod_words * 100

    if len_prod_words == len_name_words and sov <= 50:
        return

    if sov > 40:
        return get_calc_stats(product, gramm) if gramm != 100 else product


def get_product(name: str, gramm: int) -> List[dict]:
    with open('tg_app/products.json', 'r') as file:
        products_list = json.load(file)

    result = []

    for product in products_list:
        result_filter = get_filtering(product, name, gramm)
        if result_filter != None:
            result.append(result_filter)
    return result
