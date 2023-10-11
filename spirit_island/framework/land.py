class Land:
    """Class for storing the status of the Island."""

    def __init__(self):
        """Initialise."""
        self.board = "D"
        self.number = ""
        self.terrain = ""

        self.invader_count = {"city": 0, "town": 0, "explorer": 0}
        self.presence_count = {"My": 0}
        self.dahan_count = 0
        self.blight_count = 0

        self.fear_generated = 0
        self.defend = 0

    def __eq__(self, other):
        return self.board == other.board and self.number == other.number
