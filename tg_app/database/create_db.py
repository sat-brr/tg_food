from models.maindb import create_db
from models.users import User
from models.products import Product


def start():
    create_db()


if __name__ == '__main__':
    start()
