import json
import time

class CreateMessage:
    def __init__(self, msg_time, msg_fromme, msg_to, msg_action, msg_message):
        self._time = msg_time
        self._fromme = msg_fromme
        self._to = msg_to
        self._action = msg_action
        self._message = msg_message

    def create_message(self):
        mymsg = {
            'action': 'msg',
            'time': self._time,
            'to': self._to,
            'from': self._fromme,
            'encoding': 'utf-8',
            'message': self._message
        }

        return mymsg