import time
from classies.probe import CreateProbe
from classies.pack import PackMessage
from classies.verification_users import VerificationUsers
from classies.response import CreateResponse

class VerificationMessage:
    def __init__(self, msg_dict):
        self._dict = msg_dict
        self._user = ''
    
    #метод проверки сообщений
    def verification(self):
        #проверка аутентификации
        if self._dict['action'] == 'authenticate':
            user = VerificationUsers(self._dict['user']['account_name'])
            if user.ver_users():
                self._user = self._dict['user']['account_name']
                return self._user
        
        #проверка ответа на аутентификацию
        if self._dict['action'] == 'back_authenticate':
            pass

        #проверка пресенс собщения
        if self._dict['action'] == 'presence':
            print('Имя пользователя: {}'.format(self._dict['user']['account_name']))
            user = VerificationUsers(self._dict['user']['account_name'])
            if user.ver_users():
                probe = CreateProbe('probe', time.strftime('%H:%M:%S'))
                pack_probe = PackMessage(probe.create_probe())
                print('Пользователь есть')
                return pack_probe.pack()
            elif not user.ver_users():
                resp = CreateResponse(404, time.strftime('%H:%M:%S'), 'Такого пользователя не существует.')
                pack_resp = PackMessage(resp.create_response())
                print('Пользователя нет')
                return pack_resp.pack()
        
        #проверка сообщения
        if self._dict['action'] == 'msg':
            pass
            