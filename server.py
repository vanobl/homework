# -*- coding: utf-8 -*-
import os
import sys
import socket
import time
import logging, logging.config
import select
import json
from threading import Thread

#импортируем собственные классы
from classies.receive_message import ReceiveMessage
from classies.verification_message import VerificationMessage
from classies.create_friends import CreateFriends

#указываем файл логгера
logging.config.fileConfig('log.conf')
#включаем нужный логгер
log = logging.getLogger('main')

import sqlalchemy
#импортируем классы таблиц
from db.alchemy import CUsers, ListFriends, CMassages
#создаём подключение
path = os.path.join('db', 'messages.db')
engine = sqlalchemy.create_engine('sqlite:///{}'.format(path))
#создаём сессию
session = sqlalchemy.orm.sessionmaker(bind=engine)()

class Server:
    def __init__(self, port=8888):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('localhost', port))
        self.s.listen(5)
        self.s.settimeout(0.2)

        self._clients = {}
        self._adduser = Thread(target=self.user_connect)
        self._guser = Thread(target=self.user_get)
        text = u'Запуск сервера.'
        print(text)
        log.debug(text)

        #запускаем поток для подключения клиентов
        self._adduser.start()
        self._guser.start()
    
    def user_connect(self):
        while True:
            try:
                #ждём подключения
                sock_client, addr_client = self.s.accept()
                #распаковываем сообщение
                my_recv = ReceiveMessage(sock_client)
                mydict = my_recv.receive_message()
                #проверяем сообщение
                ver = VerificationMessage(mydict)
                user = ver.verification()
                #добавляем клиента и его сокет в словарь
                self._clients[user] = sock_client
                #отправляем имена пользователей клиенту
                self.send_friends(self.get_user_friends(user), self._clients[user])
            except OSError as e:
                #ошибка истечения таймаута
                pass
    
    #метод отправки пользователей для заполнения списка
    def send_friends(self, friends, sock_user):
        dict_friends = CreateFriends(friends).create_friends()
        print(dict_friends)

    def user_get(self):
        while True:
            #print(self._clients)
            time.sleep(5)
    
    #метод извлечения друзей пользователя
    def get_user_friends(self, username):
        users = session.query(ListFriends).filter_by(id_cuser = self.searh_user_id(username)).all()
        send_users = []
        for user in users:
            send_users.append(user.r_id_friend.name)
        # print('друзья пользователя: {}'.format(send_users))
        return send_users

    #метод поиска id пользователя
    def searh_user_id(self, sendname):
        find_user = session.query(CUsers).filter_by(name = sendname).first()
        return find_user.id


        # while True:
        #     try:
        #         #ждём подключения
        #         sock_client, addr_client = s.accept()
        #         #выводим сообщение о подключении
        #         #text = u'Клиент {} подключился'.format(sock_client.getsockname)
        #         text = 'Proverka'
        #         log.debug(text)
        #         print(str(sock_client.getsockname))
        #         #распаковываем сообщение
        #         my_recv = ReceiveMessage()
        #         mydict = my_recv.receive_message(sock_client)
        #         #проверяем сообщение
        #         ver = VerificationMessage(mydict)
        #         #отправляем ответ сервера
        #         sock_client.send(ver.verification())
        #     except OSError as e:
        #         #ошибка истечения таймаута
        #         pass
        #     else:
        #         clients.append(sock_client)
        #         log.debug('Клиент {} добавлен в список клиентов.'.format(addr_client))
        #     finally:
        #         pass
        #         #проверяем события без таймаута
        #         r = []
        #         w = []
        #         e = []

        #         # try:
        #         #     w, r, e = select.select(clients, clients, clients, 0)
        #         # except Exception as e:
        #         #     print(e)

        #         # #обходим список пишущих
        #         # for w_cl in w:
        #         #     try:
        #         #         #создаём экземпляр класса
        #         #         msg = ReceiveMessage()
        #         #         #преобразуем байты в словарь
        #         #         recv_dict = msg.receive_message(w_cl)
        #         #         #производим проверку сообщения
        #         #         ver_dict = VerificationMessage(recv_dict)
        #         #         #пишем в лог
        #         #         log.debug('Пользователь прислал сообщение')
        #         #         print('Пользователь прислал сообщение')
        #         #         #client.send(ver_dict)
        #         #         try:
        #         #             print('Обход слушателей')
        #         #             for r_clients in r:
        #         #                 r_clients.send(ver_dict)
        #         #         except:
        #         #             pass
        #         #     except:
        #         #         print('Клиент {} отключился'.format(w_cl))
        #         #         log.debug('Клиент отключился')
        #         #         clients.remove(w_cl)

if __name__ == '__main__':
    Server(8888)