class EndGameException(Exception):
    def __init__(self, victory: bool, message: str):
        self.victory = victory
        self.message = message


class UIException(Exception):
    def __init__(self, message: str):
        self.message = message
