import json
import time

class ReceiveMessage:
    _user_dict = {}
    def __init__(self, cln):
        self._cln = cln
    
    def receive_message(self):
        #получаем байты
        msg = self._cln.recv(1024)
        #получаем json
        jmsg = msg.decode('utf-8')
        #получаем словарь
        dict_msg = json.loads(jmsg)

        return dict_msg
    
    def work_for_dict(self):
        pass
        