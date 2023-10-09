from spiritIsland.framework.exceptions import EndGameException
from spiritIsland.framework.island import Island


class Action:
    """Base class for all actions."""

    def __init__(self, controls: dict, island: Island):
        """
        Initialise.
        :param controls: path to debug_controls file
        :param island: Island object
        """
        self._controls = controls
        self.island = island

    def check_end_game(self):
        if self.island.terror_level == 4:
            self.island.end = True
        elif self.island.terror_level == 3:
            # Check for any cities in the island object
            if not self.island.invader_count["city"]:
                self.island.end = True
        elif self.island.terror_level == 2:
            # Check for any towns/cities in the island object
            if (
                not self.island.invader_count["city"]
                and not self.island.invader_count["town"]
            ):
                self.island.end = True
        else:
            # Check for any explorers/towns/cities in the island object
            if (
                not self.island.invader_count["city"]
                and not self.island.invader_count["town"]
                and not self.island.invader_count["explorer"]
            ):
                self.island.end = True

        if self.island.end:
            raise EndGameException(victory=True)

    def test_action(self):
        """Dummy action for debugging."""
        self.check_end_game()
        print("test action done")
