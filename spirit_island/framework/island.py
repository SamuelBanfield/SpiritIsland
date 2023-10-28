import json
import os

from spirit_island.decks.invader_deck_builder import InvaderDeckBuilder

from .land import Land
from .pieces import *


class Island:
    """Class for storing the status of the Island."""

    def __init__(self, controls: dict):
        """Initialise.
        :param controls: path to debug_controls file
        """
        self._controls = controls

        self.n_players = 1

        self.lands = []

        self.id_count = 1

        self.fear_cards = 0
        self.fear_generated = 0
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

    def get_city_count(self):
        """Return the total city count on the island."""
        city_count = 0

        for land in self.lands:
            city_count += len(land.cities)

        return city_count

    def get_town_count(self):
        """Return the total town count on the island."""
        town_count = 0

        for land in self.lands:
            town_count += len(land.towns)

        return town_count

    def get_explorer_count(self):
        """Return the total explorer count on the island."""
        explorer_count = 0

        for land in self.lands:
            explorer_count += len(land.explorers)

        return explorer_count

    def generate_fear(self, fear_quantity):
        """Generate an amount of fear and check for thresholds."""
        fear_remaining = fear_quantity
        while fear_remaining > 0:
            if self.fear_generated + fear_remaining < 4 * self.n_players:
                self.fear_generated += fear_remaining
            else:
                fear_threshold = 4 * self.n_players - self.fear_generated
                fear_remaining -= fear_threshold
                self.fear_generated = 0
                self.fear_cards += 1

                self.update_terror_level()

    def update_terror_level(self):
        """Updates the terror level after a fear card had been earned"""
        return
