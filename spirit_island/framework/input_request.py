from typing import List


class InputRequest:

    def __init__(self, message):
        """
        :param message: message to be displayed in the UI explaining required input
        """
        self.message = message
        self.resolution = None

    def get_resolution(self):
        """Returns the input provided by the user"""
        return self.resolution

class InputHandler:

    def __init__(self):
        self.input_requests: List[InputRequest] = []

    def make_input_request(self, input_request: InputRequest):
        self.input_requests.append(input_request)