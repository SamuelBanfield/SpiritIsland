class Land:
    """Class for storing the status of the Island."""

    def __init__(self):
        """Initialise."""
        self.board = "D"
        self.number = ""
        self.terrain = ""

        self.cities = []
        self.towns = []
        self.explorers = []
        self.presence = []
        self.dahan = []
        self.blight = []

        self.fear_generated = 0
        self.defend = 0

    def __eq__(self, other):
        return self.board == other.board and self.number == other.number
