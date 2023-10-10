import json

from .land import Land


class Island:
    """Class for storing the status of the Island."""

    def __init__(self, controls: dict):
        """Initialise.
        :param controls: path to debug_controls file
        """
        self._controls = controls

        self.lands = []

        self.fear_cards = 0
        self.fear_generated = 0
        self.terror_level = 1

        self.end = False

    def get_lands(self):
        """Fills in the lands with land objects.
        """
        with open("../resources/board_d.json") as board_file:
            board_dict = json.load(board_file)

        for land_number in board_dict:
            new_land = Land()
            new_land.number = land_number

            for piece in board_dict[land_number]:
                if piece in ["city", "town", "explorer"]:
                    new_land.invader_count[piece] = board_dict[land_number][piece]
                elif piece == "blight":
                    new_land.blight_count = board_dict[land_number][piece]
                elif piece == "dahan":
                    new_land.dahan_count = board_dict[land_number][piece]

            self.lands.append(new_land)

    def get_city_count(self):
        """Return the total invader count on the island.
        """
        city_count = 0

        for land in self.lands:
            city_count += land.invader_count["city"]

        return city_count

    def get_town_count(self):
        """Return the total invader count on the island.
        """
        town_count = 0

        for land in self.lands:
            town_count += land.invader_count["town"]

        return town_count

    def get_explorer_count(self):
        """Return the total invader count on the island.
        """
        explorer_count = 0

        for land in self.lands:
            explorer_count += land.invader_count["explorer"]

        return explorer_count