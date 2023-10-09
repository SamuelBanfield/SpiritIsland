class Island:
    """Class for storing the status of the Island."""
    def __init__(self, controls: dict):
        """Initialise.
        :param controls: path to debug_controls file
        """
        self._controls = controls
        self.invader_count = {"city": 0, "town": 0, "explorer": 0}
        self.terror_level = 1
        self.end = False
