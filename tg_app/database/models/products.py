from typing import Any

from sqlalchemy import Column, Integer, String, select

from tg_app.database.models.crud import CrudModel
from tg_app.database.models.maindb import Base, async_db_session


class CheckName:
    @classmethod
    async def check_by_name(cls, name: str) -> Any:
        query = select(cls).where(cls.name == name)
        result = await async_db_session.execute(query)
        return result.first()

    @classmethod
    async def find_similar(cls, name: str) -> Any:
        query = select(cls).filter((cls.name).contains(name))
        result = await async_db_session.execute(query)
        return result.scalars().all()


class Product(Base, CrudModel, CheckName):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    protein = Column(Integer)
    fat = Column(Integer)
    carbohydrate = Column(Integer)
    kcal = Column(Integer)
    url = Column(String, unique=True)

    __mapper_args__ = {"eager_defaults": True}
