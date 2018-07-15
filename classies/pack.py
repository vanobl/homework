import json

class PackMessage():
    def __init__(self, msg):
        self._msg = msg
    
    def pack(self):
        #пакуем сообщение
        json_msg = json.dumps(self._msg)
        return json_msg.encode('utf-8')