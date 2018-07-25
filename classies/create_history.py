class CreateHistory:
    def __init__(self, client_from, client_to):
        self._userfrom = client_from
        self._userto = client_to
    
    def create_history(self):
        history = {
            'action': 'history',
            'userfrom': self._userfrom,
            'userto': self._userto,
        }

        return history