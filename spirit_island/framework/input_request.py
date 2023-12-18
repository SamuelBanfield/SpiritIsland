from typing import List

from spirit_island.framework.land import Land
from spirit_island.framework.exceptions import UserInterruptedException
from pygame.time import Clock

class InputRequest:

    def __init__(self, message: str, options, user_finishable: bool = False):
        """
        :param message: message to be displayed in the UI explaining required input
        :param options: the possible values the user may choose
        :param user_finishable: whether the user may mark the input as complete without
        selecting an option
        """
        self.message = message
        self.options = options
        self.resolution = {
            "result": None,
            "errors": None,
            "complete": False
        }
        self.user_finishable = user_finishable

    def get_resolution(self):
        """
        Returns the input provided by the user, throws
        interrupted exception if necessary. (user cancels
        or shutdown)
        """
        if self.resolution["errors"]:
            raise InterruptedError(self.resolution["errors"])
        if self.resolution["complete"]:
            if not self.user_finishable:
                # The UI should not allow this to happen
                raise ValueError("User marked input as complete without selecting an option")
            raise UserInterruptedException()
        if self.resolution["result"] and self.resolution["result"] not in self.options:
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
        """
        :param reason: explanation to user of what they should be selecting
        :param options: the set of options from which the user must choose

        Returns a land selected by the user, should never be called from the
        UI thread.
        """
        if self.check_busy():
            raise ValueError("Requested input while input already pending")
        self.input_request = InputRequest(
            reason,
            options
        )
        while not self.input_request.get_resolution():
            self.clock.tick(self.fps)
        input_request = self.input_request.get_resolution()
        self.input_request = None
        return input_request

    def request_land_content_input(self, reason: str, options: List[object], user_finishable = False) -> object:
        """
        :param reason: explanation to user of what they should be selecting
        :param options: the set of options from which the user must choose
        :param user_finishable: whether the user may mark the input as complete without
        selecting an option

        Returns a thing from a land (invader, dahan, token, presence etc) selected
        by the user, should never be called from the UI thread.
        """
        if self.check_busy():
            raise ValueError("Requested input while input already pending")
        if len(options) == 1 and not user_finishable:
            # Don't bother asking the user if there's only one option and they have to pick it
            return options[0]
        self.input_request = InputRequest(
            reason,
            options,
            user_finishable,
        )
        try: 
            while not self.input_request.get_resolution():
                self.clock.tick(self.fps)
            input_request = self.input_request.get_resolution()
        except UserInterruptedException as e:
            # If the user cancels the input, we need to clear the input request
            self.input_request = None
            raise e
        self.input_request = None
        return input_request
