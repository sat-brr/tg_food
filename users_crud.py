from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import User, Base


engine = create_engine('sqlite:///tgfood.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

class CheckUser():

    def check_on_phone(param):
        result = session.query(User).filter(User.user_phone == param).count()
        if result:
            return True
        else:
            return False
        
    def check_on_user_id(param):
        result = session.query(User).filter(User.user_id == param).count()
        if result:
            return True
        else:
            return False
    
    def update(param, new_data={}):
        usr = session.query(User).filter(User.user_phone == param).one()
        for key in new_data:
            if key == 'user_id':
                usr.user_id = new_data[key]
            if key == 'user_phone':
                usr.user_phone = new_data[key]
        session.add(usr)
        session.commit()
