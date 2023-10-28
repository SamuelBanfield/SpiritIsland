from .piece import Piece


class Blight(Piece):
    """Class for storing the status of a piece."""

    def __init__(self):
        super().__init__()
        self.type = "blight"
