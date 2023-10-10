from spirit_island.actions.actions_collection import *
from spirit_island.framework.island import Island
from spirit_island.phases.phases_base import Phase


class Ravage(Phase):
    """Invader ravage phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island)

    def execute_phase(self):
        self.do_ravage_action()

    def do_ravage_action(self):
        ravage_action = RavageAction(controls=self._controls, island=self.island)
        for land in self.island.lands:
            ravage_action.execute_action(land)


class Build(Phase):
    """Invader build phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island)

    def execute_phase(self):
        self.do_build_action()

    def do_build_action(self):
        build_action = BuildAction(controls=self._controls, island=self.island)
        for land in self.island.lands:
            build_action.execute_action(land)


class Explore(Phase):
    """Invader explore phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island)

    def execute_phase(self):
        self.do_explore_action()

    def do_explore_action(self):
        explore_action = ExploreAction(controls=self._controls, island=self.island)
        for land in self.island.lands:
            explore_action.execute_action(land)


class Escalation(Phase):
    """Invader escalation phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island)
