import asyncio
import json
import time

from tg_app.database.models.products import Product

path_to_json = "tg_app/products.json"


async def write_data(val) -> None:
    await Product.create(**val)


async def get_data():
    with open(path_to_json, 'r') as file:
        data = json.load(file)
    start = time.time()
    for pr in data:
        # val = list(pr.values())
        await write_data(pr)
    ft = time.time() - start
    print(ft)


async def st() -> None:
    start = time.time()
    await get_data()
    ft = time.time() - start
    print(ft)

asyncio.run(st())
