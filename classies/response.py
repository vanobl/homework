class CreateResponse():
    def __init__(self, resp_response, resp_time, resp_error):
        self._response = resp_response
        self._time = resp_time
        self._error = resp_error
    
    def create_response(self):
        myresponse = {
            'action': 'response',
            'response': self._response,
            'time': self._time,
            'error': self._error
        }

        return myresponse