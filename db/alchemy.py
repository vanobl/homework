from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

CBase = declarative_base()
engine = create_engine('sqlite:///messages.db')
# session = sessionmaker(bind=engine)()

class CUsers(CBase):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)

    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def __rep__(self):
        return 'User ({}, {})'.format(self.name, self.password)

class CMassages(CBase):
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True)
    user_from = Column(Integer(), ForeignKey('users.id'))
    user_to = Column(Integer(), ForeignKey('users.id'))
    message = Column(String())

    p_user_from = relationship('CUsers', foreign_keys=[ user_from ])
    p_user_to = relationship('CUsers', foreign_keys=[user_to])

    def __init__(self, ufrom, uto, mess):
        self.user_from = ufrom
        self.user_to = uto
        self.message = mess

    def __rep__(self):
        return 'От: {}, к: {}, сообщение: {}'.format(self.user_from, self.user_to, self.message)

class ListFriends(CBase):
    __tablename__ = 'list_friends'

    id = Column(Integer(), primary_key=True)
    id_cuser = Column(Integer(), ForeignKey('users.id'))
    id_friend = Column(Integer(), ForeignKey('users.id'))

    r_id_cuser = relationship('CUsers', foreign_keys=[id_cuser])
    r_id_friend = relationship('CUsers', foreign_keys=[id_friend])

    def __init__(self, user, friend):
        self.id_cuser = user
        self.id_friend = friend

    def __rep__(self):
        return 'Пользователь: {} друг : {}'.format(self.id_cuser, self.id_friend)


CBase.metadata.create_all(engine)