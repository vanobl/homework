#Для ​проверки​ доступности​ пользователя​ online​-сервер​ выполняет​ probe-запрос
class CreateProbe:
    def __init__(self, action, time):
        self.action = action
        self.time = time
    
    def create_probe(self):
        msg = {
            'action': self.action,
            'time': self.time
        }

        return msg