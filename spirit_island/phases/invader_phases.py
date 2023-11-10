from spirit_island.actions.invader_actions import *
from spirit_island.framework.exceptions import EndGameException
from spirit_island.framework.island import Island
from spirit_island.phases.phases_base import Phase


class Ravage(Phase):
    """Invader ravage phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, name="Ravage")

    def begin_phase(self):
        print(f"Ravage Phase: turn {self.island.turn_counter}")
        if not self.island.invader_track["ravage"]:
            self.ravage_actions: List[RavageAction] = []
        else:
            self.ravage_actions = [
                self.create_ravage_action(land) for land in self.island.lands 
                    if self.island.invader_track["ravage"].matches_land(land)
            ]

    def update(self):
        while self.ravage_actions:
            self.ravage_actions.pop(0).execute_action()
        print("Ravage Phase Complete")

    def create_ravage_action(self, land) -> RavageAction:
        return RavageAction(controls=self._controls, island=self.island, land=land)


class Build(Phase):
    """Invader build phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, name="Build")

    def begin_phase(self):
        print(f"Build Phase: turn {self.island.turn_counter}")
        if not self.island.invader_track["build"]:
            self.build_actions: List[BuildAction] = []
        else:
            self.build_actions = [
                self.create_build_action(land) for land in self.island.lands 
                    if self.island.invader_track["build"].matches_land(land)
            ]
    
    def update(self):
        while self.build_actions:
            self.build_actions.pop(0).execute_action()

        print("Build Phase Complete")

    def create_build_action(self, building_land):
        return BuildAction(controls=self._controls, island=self.island, land=building_land)


class Explore(Phase):
    """Invader explore phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, name="Explore")

    def begin_phase(self):
        print(f"Explore Phase: turn {self.island.turn_counter}")
        try:
            new_card = self.island.invader_deck.pop(0)
        except IndexError:
            raise EndGameException(
                victory=False, message="You ran out of invader cards!"
            )
        self.island.invader_track["explore"] = new_card
        self.explore_actions = [
            self.create_explore_action(land) for land in self.island.lands 
                if self.island.invader_track["explore"].matches_land(land)
        ]

    def update(self):
        while self.explore_actions:
            self.explore_actions.pop(0).execute_action()

        print("Explore Phase Complete")

    def create_explore_action(self, exploring_land):
        return ExploreAction(controls=self._controls, island=self.island, land=exploring_land)


class Escalation(Phase):
    """Invader escalation phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, name="Escalation")
