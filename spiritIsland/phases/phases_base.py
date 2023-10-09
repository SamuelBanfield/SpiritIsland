from spiritIsland.framework.island import Island


class Phase:
    """Base class for turn phases."""

    def __init__(self, controls: dict, island: Island):
        self._controls = controls
        self.island = island
