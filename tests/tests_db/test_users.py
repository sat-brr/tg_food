import asyncio
import os

import pytest

from tests.tests_db.conftest import TEST_DB_NAME, create_db
from tg_app.database.models.users import User


class TestUserCrud:

    @classmethod
    def setup_class(cls):
        asyncio.run(create_db())

    @classmethod
    def teardown_class(cls):
        os.remove(str(TEST_DB_NAME))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("tg_id, phone",
                             [(12345, 565656), (54321, 323232)])
    async def test_create_user(self, tg_id, phone):
        new_usr = await User.create(tg_id=tg_id, user_phone=phone)
        assert new_usr
        usr = await User.get(new_usr.id)
        assert new_usr is usr

    @pytest.mark.asyncio
    async def test_update_user(self):
        new_user = await User.create(tg_id=333, user_phone=9898, admin=True)
        await User.update(new_user.id, tg_id=666, user_phone=777, admin=False)

        assert new_user.tg_id == 666
        assert new_user.user_phone == 777
        assert not new_user.admin

    @pytest.mark.asyncio
    async def test_delete_user(self):
        new_user = await User.create(tg_id=333, user_phone=9898, admin=True)
        await User.delete(new_user.id)
        deleted_user = await User.get(new_user.id)
        assert not deleted_user

    @pytest.mark.asyncio
    async def test_get_by_tg_id(self):
        new_user = await User.create(tg_id=111, user_phone=111)
        user = await User.get_by_tg_id(111)
        assert new_user is user
        assert new_user.tg_id == user.tg_id
