from typing import Any

from sqlalchemy import delete, select, update

from tg_app.database.models.maindb import async_db_session


class CrudModel:

    @classmethod
    async def create(cls, **kwargs) -> None:
        new_object = cls(**kwargs)
        async_db_session.add(new_object)
        await async_db_session.commit()
        return new_object

    @classmethod
    async def update(cls, id, **kwargs) -> None:
        query = (
            update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, id) -> Any:
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        return results.scalars().first()

    @classmethod
    async def get_all(cls):
        query = select(cls)
        result = await async_db_session.execute(query)
        return result.scalars().all()

    @classmethod
    async def delete(cls, id):
        query = delete(cls).where(cls.id == id)
        await async_db_session.execute(query)
        await async_db_session.commit()
