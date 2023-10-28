from spirit_island.actions.invader_actions import *
from spirit_island.framework.exceptions import EndGameException
from spirit_island.framework.island import Island
from spirit_island.phases.phases_base import Phase


class Ravage(Phase):
    """Invader ravage phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, "Ravage")

    def execute_phase(self):
        if not self.island.invader_track["ravage"]:
            return
        for land in self.island.lands:
            if land.terrain in self.island.invader_track["ravage"].terrains:
                self.do_ravage_action(land)
            elif self.island.invader_track["ravage"].terrains == ["coast"]:
                if land.number in ["1", "2", "3"]:
                    self.do_ravage_action(land)

        print("Ravage Phase Complete")

    def do_ravage_action(self, ravaging_land):
        ravage_action = RavageAction(controls=self._controls, island=self.island)
        ravage_action.execute_action(ravaging_land)


class Build(Phase):
    """Invader build phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, "Build")

    def execute_phase(self):
        if not self.island.invader_track["build"]:
            return
        for land in self.island.lands:
            if land.terrain in self.island.invader_track["build"].terrains:
                self.do_build_action(land)
            elif self.island.invader_track["build"].terrains == ["coast"]:
                if land.number in ["1", "2", "3"]:
                    self.do_build_action(land)

        print("Build Phase Complete")

    def do_build_action(self, building_land):
        build_action = BuildAction(controls=self._controls, island=self.island)
        build_action.execute_action(building_land)


class Explore(Phase):
    """Invader explore phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, "Explore")

    def execute_phase(self):
        try:
            new_card = self.island.invader_deck.pop(0)
        except IndexError:
            raise EndGameException(
                victory=False, message="You ran out of invader cards!"
            )
        self.island.invader_track["explore"] = new_card
        for land in self.island.lands:
            if land.terrain in self.island.invader_track["explore"].terrains:
                self.do_explore_action(land)
            elif self.island.invader_track["explore"].terrains == ["coast"]:
                if land.number in ["1", "2", "3"]:
                    self.do_explore_action(land)

        print("Explore Phase Complete")

    def do_explore_action(self, exploring_land):
        explore_action = ExploreAction(controls=self._controls, island=self.island)
        explore_action.execute_action(exploring_land)


class Escalation(Phase):
    """Invader escalation phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, "Escalation")
