class CreatePresence():
    def __init__(self, pr_action, pr_time, pr_type, pr_account, pr_status):
        self._action = pr_action
        self._time = pr_time
        self._type = pr_type
        self._account = pr_account
        self._status = pr_status

    def create_presence(self):
        mypresence = {
            'action': self._action,
            'time': self._time,
            'type': self._type,
            'user': {
                'account_name': self._account,
                'status': self._status 
            }
        }

        return mypresence