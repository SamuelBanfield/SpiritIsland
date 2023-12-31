class Piece:
    """Class for storing the status of a piece."""

    def __init__(self):
        self.id = 0
        self.type = None

    def __eq__(self, other):
        return self.id == other.id
