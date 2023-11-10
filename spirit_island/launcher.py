import json
import os
from pathlib import Path
from typing import List, Union

from spirit_island.framework.island import Island
from spirit_island.framework.logger import logger
from spirit_island.phases.fear_card_phase import FearPhase
from spirit_island.phases.invader_phases import *
from spirit_island.phases.transition_phases import *


def read_json(filepath: Union[str, Path]) -> dict:
    """
    Reads a json file into a dict.
    :param: filepath: path to json file
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
        self.controls = read_json(controls_path) if controls_path else {}
        self.victory = False
        self.end_game_message = None
        self.phase_objects: List[Phase] = []
        self.current_phase_index: int = 0
        self.ravage = None
        self.build = None
        self.explore = None
        self.cards_advance = None
        self.fear_card_phase = None
        self.time_passes_phase = None
        self.island = None

        logger.info("Runner initialised")

    def create_phases(self):
        phase_list = [
            "growth_phase",
            "card_plays_phase",
            "fast_phase",
            "event_phase",
            "blighted_island_phase",
            "fear_card_phase",
            "ravage_phase",
            "build_phase",
            "explore_phase",
            "escalation_phase",
            "cards_advance_phase",
            "slow_phase",
            "time_passes_phase",
        ]
        # Make instances of each phase and store in runner
        self.fear_card_phase = FearPhase(controls=self.controls, island=self.island)
        self.phase_objects.append(self.fear_card_phase)

        self.ravage = Ravage(controls=self.controls, island=self.island)
        self.phase_objects.append(self.ravage)

        self.build = Build(controls=self.controls, island=self.island)
        self.phase_objects.append(self.build)

        self.explore = Explore(controls=self.controls, island=self.island)
        self.phase_objects.append(self.explore)

        self.cards_advance = CardsAdvance(controls=self.controls, island=self.island)
        self.phase_objects.append(self.cards_advance)

        self.time_passes_phase = TimePassesPhase(
            controls=self.controls, island=self.island
        )
        self.phase_objects.append(self.time_passes_phase)
        return

    def create_island(self):
        self.island = Island(controls=self.controls)

    def perform_phases_no_ui(self):
        """Loop through phases. Does not run through UI."""
        try:
            for phase in self.phase_objects:
                phase.begin_phase()
        except EndGameException as ege:
            self.victory = ege.victory
            self.end_game_message = ege.message
            print("Game has ended")
            return

    def perform_phase(self):
        try:
            self.phase_objects[self.current_phase_index].begin_phase()
        except EndGameException as ege:
            self.victory = ege.victory
            self.end_game_message = ege.message
            print("Game has ended")
            print(self.end_game_message)
            return
        self.current_phase_index = (self.current_phase_index + 1) % len(
            self.phase_objects
        )

    def get_current_phase(self) -> Phase:
        return self.phase_objects[self.current_phase_index]

    def perform_end_game(self):
        if self.victory:
            print("You won")
        else:
            print("You lost")
            print(f"{self.end_game_message}")


def main():
    """Main function - run Spirit Island without the UI"""
    # Path to debug controls
    controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")

    # Create the runner
    runner = Runner(controls_path)
    # Create the island, phases, and other things
    runner.create_island()
    runner.create_phases()
    # Begin the game
    for _ in range(4):
        runner.perform_phases_no_ui()
    # End the game
    runner.perform_end_game()

    print("breakpoint")


if __name__ == "__main__":
    main()
