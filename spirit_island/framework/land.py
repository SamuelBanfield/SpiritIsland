from typing import List

from spirit_island.framework.pieces import *


class Land:
    """Class for storing the status of the Island."""

    def __init__(self):
        """Initialise."""
        self.board = "D"
        self.number = ""
        self.id = ""
        self.terrain = ""

        self.cities: List[City] = []
        self.towns: List[Town] = []
        self.explorers: List[Explorer] = []
        self.presence: List[Presence] = []
        self.dahan: List[Dahan] = []
        self.blight: List[Blight] = []

        self.fear_generated_in_land = 0
        self.defend = 0
        self.dahan_defend = 0

        self.is_coastal = False
        self.can_build = True
        self.can_build_city = True

    def __eq__(self, other):
        return self.board == other.board and self.number == other.number

    def get_invader_count(self) -> int:
        return len(self.cities) + len(self.towns) + len(self.explorers)

    def get_city_count(self) -> int:
        return len(self.cities)

    def get_town_count(self) -> int:
        return len(self.towns)

    def get_explorer_count(self) -> int:
        return len(self.explorers)

    def get_dahan_count(self) -> int:
        return len(self.dahan)

    def get_blight_count(self) -> int:
        return len(self.blight)

    def reset_properties(self):
        # Temporary way of resetting properties in time passes phase
        self.defend = 0
        self.dahan_defend = 0 # Defence that only protects dahan, not the land
        self.can_build = True
        self.can_build_city = True
        self.fear_generated_in_land = 0
