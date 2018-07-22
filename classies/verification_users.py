import os
import sqlalchemy
#импортируем классы таблиц
from db.alchemy import CUsers
#создаём подключение
path = os.path.join('db', 'messages.db')
engine = sqlalchemy.create_engine('sqlite:///{}'.format(path))
#создаём сессию
session = sqlalchemy.orm.sessionmaker(bind=engine)()

class VerificationUsers():
    def __init__(self, user_name):
        self._user_name = user_name
        self._istina = False
    
    def ver_users(self):
        users = session.query(CUsers).all()

        for user in users:
            if user.name == self._user_name:
                self._istina = True
        
        return self._istina