from typing import List


class InputRequest:

    def __init__(self, message):
        self.message = message
        self.resolution = None

    def get_resolution(self):
        return self.resolution

class InputHandler:

    def __init__(self):
        self.input_requests: List[InputRequest] = []

    def make_input_request(self, input_request: InputRequest):
        self.input_requests.append(input_request)