from typing import List

from spirit_island.framework.land import Land
from pygame.time import Clock

class InputRequest:

    def __init__(self, message: str, options):
        """
        :param message: message to be displayed in the UI explaining required input
        :param options: the possible values the user may choose
        """
        self.message = message
        self.options = options
        self.resolution = {
            "result": None,
            "errors": None
        }

    def get_resolution(self):
        """
        Returns the input provided by the user, throws
        interrupted exception if necessary. (user cancels
        or shutdown)
        """
        if self.resolution["errors"]:
            raise InterruptedError(self.resolution["errors"])
        if self.resolution["result"] and not self.resolution["result"] in self.options:
            raise ValueError(
                f"User selected invalid option '{self.resolution['result']}', not in list of possible options: '{self.options}'")
        return self.resolution["result"]


class InputHandler:

    def __init__(self, fps: int):
        self.input_request: InputRequest = None
        self.clock = Clock()
        self.fps = fps

    def check_busy(self):
        return self.input_request is not None

    def request_land_input(self, reason: str, options: List[Land]) -> Land:
        if self.check_busy():
            raise ValueError("Requested input while input already pending")
        self.input_request = InputRequest(
            reason,
            options
        )
        while not self.input_request.get_resolution():
            self.clock.tick(self.fps)
        return self.input_request.get_resolution()