from typing import Literal

from tg_app.database.models.products import Product


async def get_calc_stats(product: dict, gramm: int) -> dict:
    stats = ['protein', 'fat', 'carbohydrate', 'kcal']
    res = gramm / 100

    for stat in stats:
        product[stat] = round(float(product[stat]) * res, 3)

    return product


async def filter_by_match(product_name: str,
                          name: str) -> Literal[True] | None:
    name_words = name.split()
    product_name_words = product_name.split()
    len_name_words = len(name_words)
    len_prod_name_words = len(product_name_words)
    if product_name_words[0].lower() != name_words[0].lower():
        return

    if len_prod_name_words < len_name_words:
        return

    counter = sum(word in product_name_words for word in name_words)
    result_match = counter/len_prod_name_words * 100

    if len_prod_name_words == len_name_words and result_match <= 50:
        return

    if result_match > 40:
        return True


async def find_and_calc(name, gramm=100) -> list[dict] | list:
    similar_products = await Product.find_similar(name)

    filtered_products = []

    for product in similar_products:
        product_dict = product.__dict__
        filter_result = await filter_by_match(product_dict['name'], name)

        if filter_result:
            filtered_products.append(product_dict)
    if gramm != 100 and gramm > 0:
        return [await get_calc_stats(product, gramm)
                for product in filtered_products]
    else:
        return filtered_products
