import json
import os

from spirit_island.decks.invader_deck_builder import InvaderDeckBuilder
from spirit_island.framework.land import Land
from spirit_island.framework.pieces import *


class Island:
    """Class for storing the status of the Island."""

    def __init__(self, controls: dict):
        """Initialise.
        :param controls: path to debug_controls file
        """
        self._controls = controls
        self.turn_counter = 1

        self.n_players = 1
        self.blight_pool = 1 + self.n_players * 2

        self.lands = []

        self.id_count = 1

        self.fear_cards_pending = 0
        self.fear_cards_to_next_level = 3
        self.fear_earned = 0
        self.fear_capacity = self.n_players * 4
        self.terror_level = 1

        self.invader_track = {
            "explore": None,
            "build": None,
            "ravage": None,
            "discard": [],
        }
        self.invader_deck = []

        self.end = False

        self.get_lands()
        self.get_invader_deck()

    def add_piece(self, piece_type: str, land: Land):
        """Adds a given piece type to the given land"""

        piece_dict = {
            "obj": {
                "city": City,
                "town": Town,
                "explorer": Explorer,
                "blight": Blight,
                "dahan": Dahan,
                "presence": Presence,
            },
            "list": {
                "city": land.cities,
                "town": land.towns,
                "explorer": land.explorers,
                "blight": land.blight,
                "dahan": land.dahan,
                "presence": land.presence,
            },
        }

        new_piece = piece_dict["obj"][piece_type]()
        new_piece.id = self.id_count
        self.id_count += 1

        piece_dict["list"][piece_type].append(new_piece)

    def get_lands(self):
        """Fills in the lands with land objects."""
        rel_path = os.path.relpath(__file__ + "/../../resources/board_d.json")
        with open(rel_path) as board_file:
            board_dict = json.load(board_file)

        for land_number in board_dict:
            new_land = Land()
            new_land.number = land_number
            new_land.id = new_land.board + new_land.number

            for i, (key, value) in enumerate(board_dict[land_number].items()):
                if key in ["city", "town", "explorer", "blight", "dahan"]:
                    for _ in range(value):
                        self.add_piece(key, new_land)
                elif key == "terrain":
                    new_land.terrain = value

            self.lands.append(new_land)

    def get_invader_deck(self):
        """Retrieve a generated invader deck from the invader deck builder."""
        builder = InvaderDeckBuilder()
        self.invader_deck = builder.build_deck()

    def get_city_count_island(self):
        """Return the total city count on the island."""
        island_city_count = sum(len(land.cities) for land in self.lands)

        return island_city_count

    def get_town_count_island(self):
        """Return the total town count on the island."""
        island_town_count = sum(len(land.towns) for land in self.lands)

        return island_town_count

    def get_explorer_count_island(self):
        """Return the total explorer count on the island."""
        island_explorer_count = sum(len(land.explorers) for land in self.lands)

        return island_explorer_count

    def add_fear(self, fear_added):
        """Add fear to fear pool and earn the necessary fear cards."""
        self.fear_earned += fear_added
        while self.fear_earned >= self.fear_capacity:
            self.earn_fear_card()
            self.fear_earned -= self.fear_capacity

    def earn_fear_card(self):
        """Add one to pending fear cards. Then check terror level."""
        self.fear_cards_pending += 1
        self.fear_cards_to_next_level -= 1

        self.update_terror_level()

    def update_terror_level(self):
        """Updates the terror level after a fear card had been earned"""
        if self.fear_cards_to_next_level == 0:
            self.terror_level += 1
            self.fear_cards_to_next_level = 3


"""
class TerrorHandler:
    def __init__(self):
"""
