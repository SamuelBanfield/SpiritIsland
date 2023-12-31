from spirit_island.framework.exceptions import EndGameException
from spirit_island.framework.island import Island
from spirit_island.framework.logger import logger


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
        if "suppress_end_of_game" in self._controls and self._controls["suppress_end_of_game"]:
            return
        if self.island.terror_handler.terror_level == 4:
            self.island.terror_handler.end = True
        elif self.island.terror_handler.terror_level == 3:
            # Check for any cities in the island object
            if not self.island.get_city_count_island():
                self.island.end = True
        elif self.island.terror_handler.terror_level == 2:
            # Check for any towns/cities in the island object
            if (
                not self.island.get_city_count_island()
                and not self.island.get_town_count_island()
            ):
                self.island.end = True
        else:
            # Check for any explorers/towns/cities in the island object
            if (
                not self.island.get_city_count_island()
                and not self.island.get_town_count_island()
                and not self.island.get_explorer_count_island()
            ):
                self.island.end = True

        if self.island.end:
            raise EndGameException(
                victory=True,
                message=f"Fear Victory at Terror level {self.island.terror_handler.terror_level}",
            )

    def test_action(self):
        """Dummy action for debugging."""
        self.check_end_game()
        print("test action done")
