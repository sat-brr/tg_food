import json


def get_calc_stats(product, gramm):
    stats = ['protein', 'fat', 'carbohydrate', 'kcal']
    new_prod = product
    res = gramm / 100
    for stat in stats:
        new_prod[stat] = round(float(product[stat]) * res, 3)
    return new_prod


def get_filtering(product, name, gramm):
    name_words = name.split()
    product_name = product['name']
    product_nwords = product_name.split()
    len_name_words = len(name_words)
    len_prod_words = len(product_nwords)
    counter = 0

    if product_nwords[0].lower() != name_words[0].lower():
        return

    if len_prod_words < len_name_words:
        return

    for word in name_words:
        if word in product_nwords:
            counter += 1

    sov = counter/len_prod_words * 100

    if len_prod_words == len_name_words and sov <= 50:
        return

    if sov > 40:
        if gramm != 100:
            return get_calc_stats(product, gramm)
        return product


def get_product(name, gramm):
    with open('products.json', 'r') as file:
        products_list = json.load(file)

    result = []

    for product in products_list:
        result_filter = get_filtering(product, name, gramm)
        if result_filter != None:
            result.append(result_filter)
    return result
