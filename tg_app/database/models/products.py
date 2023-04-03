from sqlalchemy import Column, String, Integer
from .maindb import Base


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    protein = Column(Integer)
    fat = Column(Integer)
    carbohydrate = Column(Integer)
    kcal = Column(Integer)
    url = Column(String, unique=True)
    
    def __init__(self, name, protein=None, fat=None, carbohydrate=None, kcal=None, url=None)-> None:
        self.name = name
        self.protein = protein
        self.fat = fat
        self.carbohydrate = carbohydrate
        self.kcal = kcal
        self.url = url
