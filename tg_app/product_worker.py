from typing import Literal

from tg_app.database.models.products import Product


async def calc_stats(product: dict, gramm: int) -> dict:
    stats = ['protein', 'fat', 'carbohydrate', 'kcal']
    res = gramm / 100

    for stat in stats:
        if product[stat] != 0:
            product[stat] = round(float(product[stat]) * res, 3)

    return product


async def filter_by_match(product_name: str,
                          name: str) -> Literal[True] | None:
    name_words = name.split()
    product_name_words = product_name.split()
    len_name_words = len(name_words)
    len_prod_name_words = len(product_name_words)
    if product_name_words[0] != name_words[0]:
        return

    if len_prod_name_words < len_name_words:
        return

    counter = sum(word in product_name_words for word in name_words)
    result_match = counter/len_prod_name_words * 100

    if len_prod_name_words == len_name_words and result_match <= 50:
        return

    if result_match > 40:
        return True


async def find_similar_products(search_name: str) -> list[dict] | None:
    similar_products = await Product.find_similar(search_name)
    if not similar_products:
        return
    similar_products = [x.__dict__ for x in similar_products]
    similar_products = [
        ({key: val for key, val in products.items()
          if key != '_sa_instance_state'})
        for products in similar_products
        ]
    return similar_products


async def get_filtered_products(similar_products, search_name):
    result = []
    for product in similar_products:
        filter_result = await filter_by_match(product['name'].upper(),
                                              search_name)
        if filter_result:
            result.append(product)
    return result


async def parse_message(usr_message: str) -> tuple[str, int]:
    message = usr_message.split(',')
    gram = 100
    if 1 < len(message) < 3:
        try:
            gram = int(message[1])
        except Exception:
            pass

    return message[0].upper(), gram


async def find_and_calc(usr_message: str):
    search_name, gram = await parse_message(usr_message)
    similar_products = await find_similar_products(search_name)

    if not similar_products:
        return

    filtered_products = await get_filtered_products(similar_products,
                                                    search_name)

    if gram == 100 or gram <= 0:
        return filtered_products, gram

    prods_with_new_stats = [await calc_stats(prod, gram)
                            for prod in filtered_products]
    return prods_with_new_stats, gram
