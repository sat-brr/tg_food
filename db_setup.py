import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

engine = create_engine('sqlite:///tgfood.db')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    user_phone = Column(Integer, unique=True)


Base.metadata.create_all(engine)
