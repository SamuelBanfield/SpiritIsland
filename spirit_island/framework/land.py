class Land:
    """Class for storing the status of the Island."""

    def __init__(self):
        """Initialise.
        """
        self.board = "D"
        self.number = ""

        self.invader_count = {"city": 0, "town": 0, "explorer": 0}
        self.presence_count = {"My": 0}
        self.dahan_count = 0
        self.blight_count = 0
