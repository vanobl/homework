import sqlalchemy
#импортируем классы таблиц
from db.alchemy import CUsers
#создаём подключение
engine = sqlalchemy.create_engine('sqlite:///db/messages.db')
#создаём сессию
session = sqlalchemy.orm.sessionmaker(bind=engine)()

class VerificationUsers():
    def __init__(self, user_name):
        self.user_name = user_name
        self.istina = False
    
    def ver_users(self):
        users = session.query(CUsers).all()

        for user in users:
            if user.name == self.user_name:
                return True
        
        return self.istina