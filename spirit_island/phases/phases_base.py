from spirit_island.framework.island import Island


class Phase:
    """Base class for turn phases."""

    def __init__(self, controls: dict, island: Island, name: str = "Unnamed phase"):
        self._controls = controls
        self.island = island
        self._name = name
        self.is_complete = True

    def get_name(self):
        return self._name

    def begin_phase(self):
        """Called at the beginning of the phase to initialise"""
        pass

    def update(self):
        """
        Called every frame until

        It's probably worth thinking about calling this less often
        """
        pass
