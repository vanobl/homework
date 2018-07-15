import tkinter
from tkinter.ttk import Treeview
from tkinter import messagebox

import socket
import json
import time

import sqlalchemy
#импортируем классы таблиц
from db.alchemy import CUsers, ListFriends
#создаём подключение
engine = sqlalchemy.create_engine('sqlite:///db/messages.db')
#создаём сессию
session = sqlalchemy.orm.sessionmaker(bind=engine)()

#импортируем свои классы
from classies.create_message import CreateMessage
from classies.presence import CreatePresence
from classies.pack import PackMessage
from classies.receive_message import ReceiveMessage

class ClientGUI:
    def __init__(self, main):
        #определяем объект для списка друзей
        self.tree = Treeview()
        self.tree.heading('#0', text='Друзья')
        self.tree.grid(row=0, column=0)

        #определяем главное меню
        self.main = main
        self.main_menu = tkinter.Menu(self.main)
        self.main.configure(menu=self.main_menu)

        #определим пункты главного меню
        self.first_item = tkinter.Menu(self.main_menu, tearoff=0)

        #определим подпункты
        self.first_item.add_command(label='Подключиться', command=self.check)
        self.first_item.add_command(label='Заполнить', command=self.viewing_users)
        self.first_item.add_separator()
        self.first_item.add_command(label='Выход', command=self.exit_app)

        #прикрепляем пункты к главному меню
        self.main_menu.add_cascade(label='Файл', menu=self.first_item)


    #заполняем таблицу пользователей
    def viewing_users(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        users = session.query(ListFriends).filter_by(id_cuser = 1).all()
        for user in users:
            self.tree.insert('', 0, text=user.r_id_friend.name)
    
    #выход из приложения
    def exit_app(self):
        self.main.destroy()
    
    #диалоговое окно
    def check(self):
        win = tkinter.Toplevel(self.main)
        lbl = tkinter.Label(win, text='Введите логин')
        lbl.grid(row=0, column=0)
        entry = tkinter.Entry(win)
        entry.grid(row=1, column=0)
        btn = tkinter.Button(win, text='Войти')
        btn.grid(row=2, column=0)
    
    #нажатие на кнопку подключения
    def get_name(self):
        pass
    
    #подключение к серверу
    def init_connection(self, user_name):
        #создаём сокет
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #выводим запрос на ввод ip
        foreingn_ip = input('Введите IP-адрес в формате (0.0.0.0): ')
        #подключаемся к нужному адресу
        s.connect((foreingn_ip, 8888))

        #выводим запрос на ввод логина
        account_name = user_name

        #подготавливаем presence сообщение
        press = CreatePresence('presence', time.strftime('%H:%M:%S'), 'status', account_name, 'I\'m here')
        #запаковываем сообщение
        jmsg = PackMessage(press.create_presence())
        #отправляем presence сообщение
        s.send(jmsg.pack())

root = tkinter.Tk()
root.title('Клиент мессенджера')
root.geometry('640x480')

cln = ClientGUI(root)


root.mainloop()