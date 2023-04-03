from typing import List
from sqlalchemy import Column, Integer, Boolean
from tg_app.database.models.maindb import Session
from tg_app.database.models.maindb import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    user_phone = Column(Integer, unique=True)
    admin = Column(Boolean, unique=False, default=False)
    
    def __init__(self, user_id: int, user_phone: int, admin=False) -> None:
        self.user_id = user_id
        self.user_phone = user_phone
        self.admin = admin
        self.sess = Session()


class CheckUser:
    sess= Session()
    usr = User
    table = sess.query(usr)

    def check_by_phone(self, phone) -> bool:
        return bool(self.table.filter(self.usr.user_id==phone).first())

    def check_by_user_id(self, usr_id) -> bool:
        return bool(self.table.filter(self.usr.user_id==usr_id).first())

    def check_admin(self, usr_id: int):
        user = self.table.filter(self.usr.user_id==usr_id).first()
        return bool(user.admin)


class CrudUser(CheckUser):
    
    def create_user(self, *args: tuple) -> None:
        self.sess.add(self.usr(*args))
        self.sess.commit()
        self.sess.close()
    
    def update_user(self, user_id: int, params: list[tuple]) -> None:
        usr = self.table.filter(self.usr.user_id==user_id).first()
        for param in params:
            if param[0] == 'user_phone':
                usr.user_phone = param[1]
            elif param[0] == 'admin':
                usr.admin = bool(param[1])
        self.sess.add(usr)
        self.sess.commit()
        self.sess.close()

    def delete_user(self, user_id: int) -> None:
        usr = self.table.filter(self.usr.user_id==user_id).first()
        self.sess.delete(usr)
        self.sess.commit()
        self.sess.close()
