# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QCoreApplication
import sys
import os
import socket

#импортируем свобственные классы
from classies.authenticate import Authenticate
from classies.pack import PackMessage

import sqlalchemy
#импортируем классы таблиц
from db.alchemy import CUsers, ListFriends, CMassages
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

        #создаём сокет
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #подключаемся к нужному адресу
        self.s.connect(('localhost', 8888))

        #назначим подксказки
        self.window.btn_login.setToolTip('Кнопка для заполнения списка.')
        self.window.textEdit.setToolTip('Окно для <b>выбранных</b> друзей.')

        #назначим действия для объектов
        self.window.btn_login.clicked.connect(self.login)
        self.window.contactView.clicked.connect(self.set_text)
        self.window.select_exit.toggled.connect(QCoreApplication.instance().quit)
        self.window.btn_add_friend.clicked.connect(self.add_friend)
    
    #переносим выделенного друга в текстовое поле
    def set_text(self, index):
        #вытаскиваем все сообщения из базы
        #в будущем надо будет оптимизировать
        mess = session.query(CMassages).all()
        #получаем  id выбранного пользователя в списке пользователей
        userid = self.searh_user_id(self.window.contactView.model().data(index))
        #добавляем id просто для тестирования
        self.window.textEdit.append(str(userid))
        #формат на будущее
        format = QtGui.QTextBlockFormat()
        #перебираем сообщения
        for msg in mess:
            if msg.user_to == userid:
                #записываем сообщение от друга
                friend_text = '{}'.format(msg.message)
                self.window.textEdit.append(friend_text)
                if msg.user_from == self.searh_user_id(self.polzovatel):
                    #записываем сообщение от себя
                    my_text = '{}'.format(msg.message)
                    self.window.textEdit.append(my_text)
    
    #обработка нажатия кнопки входа
    def login(self):
        self.polzovatel = self.window.in_login.text()
        auth = Authenticate(self.polzovatel)
        user = auth.create_authenticate()
        msg_pack = PackMessage(user)
        self.s.send(msg_pack.pack())
        #self.set_text_viev()
        self.slush()
    
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
    

    #метод слушателя

    def slush(self):
        while True:
            pass