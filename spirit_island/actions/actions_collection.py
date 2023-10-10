from spirit_island.actions.action_base import Action
from spirit_island.framework.island import Island


class RavageAction(Action):
    """Ravage action in a single land."""

    def __init__(self, controls: dict, island: Island):
        """
        Initialise.
        :param controls: path to debug_controls file
        :param island: Island object
        """
        super().__init__(controls, island)

    def execute_action(self):
        """Put some action here."""
        self.check_end_game()
        print("action done")
