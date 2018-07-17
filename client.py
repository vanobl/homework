import socket
import json
import time
import logging, logging.config
from threading import Thread
#импортируем собственные классы
from classies.create_message import CreateMessage
from classies.presence import CreatePresence
from classies.pack import PackMessage
from classies.receive_message import ReceiveMessage

#метод выхода
def exit():
    s.close()

#указываем файл логгера
logging.config.fileConfig('log.conf')
#включаем нужный логгер
log = logging.getLogger('client')

#создаём сокет
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#выводим запрос на ввод ip
foreingn_ip = input('Введите IP-адрес в формате (0.0.0.0): ')
#подключаемся к нужному адресу
s.connect((foreingn_ip, 8888))

#выводим запрос на ввод логина
account_name = input('Введите свой логин: ')

#подготавливаем presence сообщение
press = CreatePresence('presence', time.strftime('%H:%M:%S'), 'status', account_name, 'I\'m here')
#запаковываем сообщение
jmsg = PackMessage(press.create_presence())
#отправляем presence сообщение
s.send(jmsg.pack())

print('Переход в режим слушателя.')
def read_client():
    while True:
        clmsg = ReceiveMessage()
        msg = clmsg.receive_message(s)
        if msg['action'] == 'probe':
            print('Сервер получил сообщение в: {}'.format(msg['time']))
        if msg['action'] == 'response':
            print(msg['error'])
            vopros = input('Создать нового пользователя? (y/n) ')
            if vopros == 'y':
                pass
            elif vopros == 'n':
                exit()
            else:
                print('Введены не верные данные.')

#отключаемся от сервера
#s.close()