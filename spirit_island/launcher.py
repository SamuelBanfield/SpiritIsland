import json
import os
from pathlib import Path

from spirit_island.framework.exceptions import EndGameException
from spirit_island.framework.island import Island
from spirit_island.phases.invader_phases import *
from spirit_island.phases.transition_phases import *


def read_json(filepath: str) -> dict:
    """
    Reads a json file into a dict
    :param filepath: path to json file
    :return: dictionary of json file contents
    """
    with open(Path(filepath), "r") as file:
        json_dict = json.load(file)
    return json_dict


class Runner:
    """Class for running the game"""

    def __init__(self, controls_path: str):
        """
        Initialise.
        :param controls_path: path to debug_controls file
        """
        self.controls = read_json(controls_path)
        self.victory = False
        self.phase_objects = []
        self.ravage = None
        self.build = None
        self.explore = None
        self.cards_advance = None
        self.island = None

        print("Runner initialised")

    def create_phases(self):
        phase_list = [
            "growth_phase",
            "card_plays_phase",
            "fast_phase",
            "event_phase",
            "fear_card_phase",
            "ravage_phase",
            "build_phase",
            "explore_phase",
            "escalation_phase",
            "cards_advance_phase"
            "slow_phase",
            "time_passes_phase",
        ]
        # Make instances of each phase and store in runner
        self.ravage = Ravage(controls=self.controls, island=self.island)
        self.phase_objects.append(self.ravage)

        self.build = Build(controls=self.controls, island=self.island)
        self.phase_objects.append(self.build)

        self.explore = Explore(controls=self.controls, island=self.island)
        self.phase_objects.append(self.explore)

        self.cards_advance = CardsAdvance(controls=self.controls, island=self.island)
        self.phase_objects.append(self.cards_advance)
        return

    def create_island(self):
        self.island = Island(controls=self.controls)

    def perform_phases(self):
        try:
            for phase in self.phase_objects:
                phase.execute_phase()
        except EndGameException as ege:
            self.victory = ege.victory
            print("Game has ended")
            return

    def perform_end_game(self):
        if self.victory:
            print("You won")
        else:
            print("You lost")


def main():
    """Main function - run Spirit Island"""
    # Path to debug controls
    controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")

    # Create the runner
    runner = Runner(controls_path)
    # Create the island, phases, and other things
    runner.create_island()
    runner.create_phases()
    # Begin the game
    for _ in range(4):
        runner.perform_phases()
    # End the game
    runner.perform_end_game()

    print("breakpoint")


if __name__ == "__main__":
    main()
