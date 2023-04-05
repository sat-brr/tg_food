from typing import Any

from sqlalchemy import select, update

from tg_app.database.models.maindb import async_db_session


class CrudModel:

    @classmethod
    async def create(cls, **kwargs) -> None:
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()

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
        return results.first()
