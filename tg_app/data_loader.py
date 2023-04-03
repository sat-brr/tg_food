import json
from database.models.maindb import Session
from tg_app.database.models.products import Product



path_to_json = 'products.json'

def load_data_in_base(session: Session, path: str) -> None: 
    with open(path, 'r') as file:
        data = json.load(file)

    for prod in data:
        values = list(prod.values())
        session.add(Product(*values))
    session.commit()
    session.close()


def main() -> None:
    load_data_in_base(Session(), path_to_json)


if __name__ == '__main__':
    main()