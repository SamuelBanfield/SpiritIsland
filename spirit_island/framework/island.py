import json
import os

from spirit_island.decks.invader_deck_builder import InvaderDeckBuilder

from .land import Land


class Island:
    """Class for storing the status of the Island."""

    def __init__(self, controls: dict):
        """Initialise.
        :param controls: path to debug_controls file
        """
        self._controls = controls

        self.n_players = 1

        self.lands = []
        self.get_lands()

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
        self.get_invader_deck()

        self.end = False

    def get_lands(self):
        """Fills in the lands with land objects."""
        rel_path = os.path.relpath(__file__ + "/../../resources/board_d.json")
        with open(rel_path) as board_file:
            board_dict = json.load(board_file)

        for land_number in board_dict:
            new_land = Land()
            new_land.number = land_number

            for attribute in board_dict[land_number]:
                if attribute in ["city", "town", "explorer"]:
                    new_land.invader_count[attribute] = board_dict[land_number][
                        attribute
                    ]
                elif attribute == "blight":
                    new_land.blight_count = board_dict[land_number][attribute]
                elif attribute == "dahan":
                    new_land.dahan_count = board_dict[land_number][attribute]
                elif attribute == "terrain":
                    new_land.terrain = board_dict[land_number][attribute]

            self.lands.append(new_land)

    def get_invader_deck(self):
        """Retrieve a generated invader deck from the invader deck builder."""
        builder = InvaderDeckBuilder()
        self.invader_deck = builder.build_deck()

    def get_city_count(self):
        """Return the total invader count on the island."""
        city_count = 0

        for land in self.lands:
            city_count += land.invader_count["city"]

        return city_count

    def get_town_count(self):
        """Return the total invader count on the island."""
        town_count = 0

        for land in self.lands:
            town_count += land.invader_count["town"]

        return town_count

    def get_explorer_count(self):
        """Return the total invader count on the island."""
        explorer_count = 0

        for land in self.lands:
            explorer_count += land.invader_count["explorer"]

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
