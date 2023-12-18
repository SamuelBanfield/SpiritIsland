from spirit_island.framework.input_request import InputHandler, InputRequest
from spirit_island.framework.land import Land

from overrides import override
from typing import List

class TestInputHandler(InputHandler):

    def __init__(self):
        super().__init__(1)
        self._expected_requests = []

    def add_expected_request(self, selection, options = None, reason = None):
        """
        :param selection: the option the input handler should select
        :param options: optional, list of the options. The handler will assert
        the presented options match these
        :param reason: optional, the handler will assert the presented reason
        matches this.
        """
        if selection is None:
            raise ValueError("Selection may not be None")
        self._expected_requests.append({
            "selection": selection,
            "options": options,
            "reason": reason
        })

    @override
    def check_busy(self):
        '''
        Overridden for test convenience

        Otherwise we set the result value then get a busy error
        when we request_land_input().
        '''
        return False

    @override
    def request_land_content_input(self, reason: str, options: List[object], user_finishable = False) -> object:
        return self._request_input(reason, options)

    @override
    def request_land_input(self, reason: str, options: List[Land]) -> Land:
        return self._request_input(reason, options)

    def _request_input(self, reason: str, options: List[object]) -> object:
        if not self._expected_requests:
            raise AssertionError(f"Unexpected request for input with reason: {reason}")
        next_expected_request = self._expected_requests.pop(0)

        # Assert the options are as expected
        if next_expected_request["options"] is not None:
            assert (
                len(options) == len(next_expected_request["options"])
            ), f"Unexpected number of options, got: {len(options)}, expected {len(next_expected_request['option'])}"
            assert (
                set(options) == set(next_expected_request['option'])
            ), f"Unexpected options, got: {set(options)}, expected {set(next_expected_request['option'])}"
    
        # Assert the reason is as expected
        if next_expected_request["reason"] is not None:
            assert (
                reason == next_expected_request["reason"]
            ), f"Unexpected reason, got: {reason}, expected {next_expected_request['reason']}"

        return next_expected_request["selection"]
