from spirit_island.actions.invader_actions import *
from spirit_island.framework.island import Island
from spirit_island.phases.phases_base import Phase


class CardsAdvance(Phase):
    """Invader cards advance along the track phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, name="Cards Advance")

    def execute_phase(self):
        track = self.island.invader_track
        if track["ravage"]:
            track["discard"].append(track["ravage"])
        if track["build"]:
            track["ravage"] = track["build"]
        if track["explore"]:
            track["build"] = track["explore"]
        track["explore"] = None

        print("Invader cards advanced")

        # Advance turn counter, will go in time passes phase eventually
        self.island.turn_counter += 1
