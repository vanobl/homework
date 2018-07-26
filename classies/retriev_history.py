import os
import sqlalchemy
from sqlalchemy import or_, and_
#импортируем классы таблиц
from db.alchemy import CUsers, CMassages
#создаём подключение
path = os.path.join('db', 'messages.db')
engine = sqlalchemy.create_engine('sqlite:///{}'.format(path))
#создаём сессию
session = sqlalchemy.orm.sessionmaker(bind=engine)()

class RetrievHistory:
    def __init__(self, userfrom, userto):
        self._userfrom = userfrom
        self._userto = userto
    
    def retriev_history(self):
        uf = session.query(CUsers).filter_by(name=self._userfrom).first()
        ut = session.query(CUsers).filter_by(name=self._userto).first()
        #messages = session.query(CMassages).filter_by(user_from=uf.id).all()
        messages = session.query(CMassages).filter(or_(and_(CMassages.user_from == uf.id, CMassages.user_to == ut.id), and_(CMassages.user_from == ut.id, CMassages.user_to == uf.id))).all()
        return messages