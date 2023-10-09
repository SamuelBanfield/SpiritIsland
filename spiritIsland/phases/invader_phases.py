from spiritIsland.actions.actions_collection import *
from spiritIsland.framework.island import Island
from spiritIsland.phases.phases_base import Phase


class Ravage(Phase):
    """Invader ravage phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island)

    def execute_phase(self):
        self.do_ravage_action()

    def do_ravage_action(self):
        ravage_action = RavageAction(controls=self._controls, island=self.island)
        ravage_action.execute_action()


class Build(Phase):
    """Invader build phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island)


class Explore(Phase):
    """Invader explore phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island)


class Escalation(Phase):
    """Invader escalation phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island)
