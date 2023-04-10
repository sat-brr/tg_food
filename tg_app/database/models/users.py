from typing import Any
from sqlalchemy import Boolean, Column, Integer, select

from tg_app.database.models.crud import CrudModel
from tg_app.database.models.maindb import Base, async_db_session


class CheckField:
    @classmethod
    async def check_by_phone(cls, phone) -> Any:
        query = select(cls).where(cls.user_phone == phone)
        result = await async_db_session.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_by_tg_id(cls, tg_id) -> Any:
        query = select(cls).where(cls.tg_id == tg_id)
        results = await async_db_session.execute(query)
        return results.scalars().first()


class User(Base, CrudModel, CheckField):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    user_phone = Column(Integer, unique=True)
    admin = Column(Boolean, unique=False, default=False)
