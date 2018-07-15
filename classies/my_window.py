from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QCoreApplication
import sys
import os

import sqlalchemy
#импортируем классы таблиц
from db.alchemy import CUsers, ListFriends
#создаём подключение
engine = sqlalchemy.create_engine('sqlite:///db/messages.db')
#создаём сессию
session = sqlalchemy.orm.sessionmaker(bind=engine)()

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        path = os.path.join('mygui', 'main.ui')
        self.window = uic.loadUi(path, self)
        self.polzovatel = ''

        #назначим подксказки
        self.window.btn_2.setToolTip('Кнопка для заполнения списка.')
        self.window.textEdit.setToolTip('Окно для <b>выбранных</b> друзей.')

        #назначим действия для объектов
        self.window.btn_2.clicked.connect(self.login)
        self.window.contactView.clicked.connect(self.set_text)
        self.window.select_exit.toggled.connect(QCoreApplication.instance().quit)
        self.window.btn_3.clicked.connect(self.add_friend)
    
    #переносим выделенного друга в текстовое поле
    def set_text(self, index):
        session.query(CMassages)
        self.window.textEdit.append(self.window.contactView.model().data(index))
    
    #обработка нажатия кнопки входа
    def login(self):
        self.polzovatel = self.window.in_login.text()
        self.set_text_viev()
    
    #заполняем список друзей
    def set_text_viev(self):
        users = session.query(ListFriends).filter_by(id_cuser = self.searh_user_id(self.polzovatel)).all()
        model = QtGui.QStandardItemModel()
        for user in users:
            model.appendRow(QtGui.QStandardItem(user.r_id_friend.name))
        self.window.contactView.setModel(model)
        self.add_item_combo()

    #заполняем ComboBox с пользователями
    def add_item_combo(self):
        users = session.query(CUsers).all()
        for user in users:
            if user.name != self.polzovatel:
                self.window.list_users.addItem(user.name)
    
    #добавляем пользователя в список друзей
    def add_friend(self):
        select_user = self.window.list_users.currentText()
        new_friend = ListFriends(self.searh_user_id(self.polzovatel), self.searh_user_id(select_user))
        session.add(new_friend)
        session.commit()
        self.set_text_viev()
    
    #метод поиска id пользователя
    def searh_user_id(self, sendname):
        find_user = session.query(CUsers).filter_by(name = sendname).first()
        return find_user.id