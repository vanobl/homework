import time

class Authenticate():
    def __init__(self, name):
        self._name = name
        self._action = 'authenticate'
        self._time = time.strftime('%H:%M:%S')
    
    def create_authenticate(self):
        authenticate = {
            'action': self._action,
            'time': self._time,
            'user': {
                "account_name" : self._name,
                "password" : "CorrectHorseBatterStaple"
            }
        }

        return authenticate