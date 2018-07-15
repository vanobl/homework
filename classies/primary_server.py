import socket
import time
import logging, logging.config
import select
import json
import os

from classies.receive_message import ReceiveMessage

#указываем файл логгера
logging.config.fileConfig(os.path.join('../', 'log.conf'))
#включаем нужный логгер
log = logging.getLogger('main')

class Server:
    def __init__(self, port=8888):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))
        s.listen(5)
        s.settimeout(0.2)

        clients = []

        log.debug('Запуск сервера.')

        while True:
            try:
                #ждём подключения
                client, addr = s.accept()
                log.debug('Клиент {} подключился'.format(addr))
            except OSError as e:
                #ошибка истечения таймаута
                pass
            else:
                clients.append(client)
                log.debug('Клиент {} добавлен в список клиентов.'.format(addr))
            finally:
                #проверяем события без таймаута
                r = []
                w = []
                e = []

                try:
                    w, r, e = select.select(clients, clients, clients, 0)
                except Exception as e:
                    print(e)

                #обходим список пишущих
                for w_cl in w:
                    try:
                        #создаём экземпляр класса
                        msg = ReceiveMessage()
                        #преобразуем байты в словарь
                        recv_dict = msg.receive_message(w_cl)
                        #сделать проверку сообщения здесь или вынести в отдельный класс?
                        #пишем в лог
                        log.debug('Пользователь прислал сообщение')
                    except:
                        print('Клиент {} отключился'.format(w_cl))
                        log.debug('Клиент отключился')
                        clients.remove(w_cl)

if __name__ == '__main__':
    Server(8888)