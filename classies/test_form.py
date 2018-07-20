#import sys
import os
import socket

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QListView, QLineEdit, QTextEdit
from PySide2.QtCore import QFile, QObject

#импортируем свобственные классы
from classies.authenticate import Authenticate
from classies.pack import PackMessage

class Form(QObject):
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        self.ui_file = QFile(ui_file)
        self.ui_file.open(QFile.ReadOnly)
        self.polzovatel = ''

        self.loader = QUiLoader()
        self.window = self.loader.load(self.ui_file)
        self.ui_file.close()

        #создаём сокет
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #подключаемся к нужному адресу
        self.s.connect(('localhost', 8888))

        #определим элементы управления
        self.btn_login = self.window.findChild(QPushButton, 'btn_login')
        self.contact_view = self.window.findChild(QListView, 'contactView')
        self.line_login = self.window.findChild(QLineEdit, 'in_login')
        self.win_chat = self.window.findChild(QTextEdit, 'win_chat')
        self.text_input = self.window.findChild(QTextEdit, 'text_input')
        self.btn_send = self.window.findChild(QPushButton, 'btn_send')

        #назначим подсказки для элементов управления
        self.btn_login.setToolTip('Кнопка входа')
        self.contact_view.setToolTip('Окно друзей')
        self.line_login.setToolTip('Строка для ввода логина')
        self.win_chat.setToolTip('Окно для вывода сообщений')
        self.text_input.setToolTip('Окно для ввода сообщения')
        self.btn_send.setToolTip('Кнопка отправки сообщения')

        #назначим коннекторы для объектов
        self.btn_login.clicked.connect(self.login)

        self.window.show()

    #обработка нажатия кнопки входа
    def login(self):
        #сохраним имя пользователя в переменную
        self.polzovatel = self.line_login.text()
        auth = Authenticate(self.polzovatel)
        user = auth.create_authenticate()
        msg_pack = PackMessage(user)
        self.s.send(msg_pack.pack())