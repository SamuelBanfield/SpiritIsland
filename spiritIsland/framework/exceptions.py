class EndGameException(Exception):
    def __init__(self, victory: bool):
        self.victory = victory
