class Land:
    """Class for storing the status of the Island."""

    def __init__(self):
        """Initialise."""
        self.board = "D"
        self.number = ""
        self.id = ""
        self.terrain = ""

        self.cities = []
        self.towns = []
        self.explorers = []
        self.presence = []
        self.dahan = []
        self.blight = []

        self.fear_generated_in_land = 0
        self.defend = 0

    def __eq__(self, other):
        return self.board == other.board and self.number == other.number

    def get_invader_count(self) -> int:
        return len(self.cities) + len(self.towns) + len(self.explorers)

    def get_city_count(self) -> int:
        return len(self.cities)

    def get_town_count(self) -> int:
        return len(self.towns)

    def get_explorer_count(self) -> int:
        return len(self.explorers)

    def get_dahan_count(self) -> int:
        return len(self.dahan)

    def get_blight_count(self) -> int:
        return len(self.blight)
