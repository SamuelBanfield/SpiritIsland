from spirit_island.framework.island import Island


class Phase:
    """Base class for turn phases."""

    def __init__(self, controls: dict, island: Island, name: str = "Unnamed phase"):
        self._controls = controls
        self.island = island
        self._name = name

    def get_name(self):
        return self._name
