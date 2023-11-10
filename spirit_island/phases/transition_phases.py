from spirit_island.actions.invader_actions import *
from spirit_island.framework.island import Island
from spirit_island.phases.phases_base import Phase


class CardsAdvance(Phase):
    """Invader cards advance along the track phase."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, name="Cards Advance")

    def begin_phase(self):
        track = self.island.invader_track
        if track["ravage"]:
            track["discard"].append(track["ravage"])
        if track["build"]:
            track["ravage"] = track["build"]
        if track["explore"]:
            track["build"] = track["explore"]
        track["explore"] = None

        print("Invader cards advanced")


class TimePassesPhase(Phase):
    """All effects that last until the end of turn are reset."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, name="Time Passes")

    def begin_phase(self):
        for land in self.island.lands:
            # Reset land properties
            land.reset_properties()
            # Reset health and damage of pieces
            for piece in land.dahan + land.cities + land.towns + land.explorers:
                piece.reset_health()
                piece.reset_damage()

        print(f"End of turn {self.island.turn_counter}")

        # Advance turn counter
        self.island.turn_counter += 1
