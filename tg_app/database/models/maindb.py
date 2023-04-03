from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///tg_app/tgfood.db')
Session = sessionmaker(bind=engine)


def create_db() -> None:
    Base.metadata.create_all(engine)

