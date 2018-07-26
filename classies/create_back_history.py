class CreateBackHistory:
    def __init__(self, history):
        self._history = history
    
    #ответ на запрос истории
    def back_history(self):
        history = {
            'action': 'back_history',
            'history': self._history,
        }

        return history