class CreateFriends:
    def __init__(self, friends):
        self._friends = friends
        #self.create_friends()
    
    def create_friends(self):
        friends = {
            'action': 'back_authenticate',
            'friends': self._friends,
        }

        return friends