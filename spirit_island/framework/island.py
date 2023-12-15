import json
import os
from typing import List

from spirit_island.decks.invader_deck_builder import InvaderDeckBuilder
from spirit_island.framework.land import Land
from spirit_island.framework.pieces import *
from spirit_island.framework.terror_hander import TerrorHandler
from spirit_island.framework.input_request import InputHandler
from spirit_island.framework.logger import logger


class Island:
    """Class for storing the status of the Island."""

    def __init__(self, controls: dict, input_handler: InputHandler):
        """Initialise.
        :param controls: path to debug_controls file
        """
        self._controls = controls
        self._input_handler = input_handler
        self.turn_counter = 1

        self.n_players = 1
        self.blight_pool = 1 + self.n_players * 2

        self.lands: List[Land] = []

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
        self.terror_handler = None

        self.end = False

        self.get_lands()
        self.get_invader_deck()
        self.create_terror_handler()

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

    def add_blight(self, land: Land, with_cascade: bool = True):
        """
        :param land: the land
        :param with_cascade: whether the blight should cascade
        """
        cascading = len(land.blight) > 0 and with_cascade
        self.add_piece("blight", land)
        if cascading:
            land_options = [other for other in self.lands if self.are_lands_adjacent(land, other) and other.number != "0"]
            cascading_land = self._input_handler.request_land_input(
                "Select land for blight cascade",
                land_options
            )
            logger.info(f"Cascading blight into land '{cascading_land.id}'")
            self.add_blight(cascading_land, True)

    def get_lands(self):
        """Fills in the lands with land objects."""
        board = self._controls["board"] if "board" in self._controls else "board_d.json"
        board_json_path = os.path.relpath(__file__ + f"/../../resources/{board}")
        with open(board_json_path) as board_file:
            board_dict = json.load(board_file)
        adjacency_file_path = os.path.relpath(__file__ + "/../../resources/board_adjacencies.json")
        with open(adjacency_file_path) as adjacency_file:
            self.adjacency_dict = {
                "D" + land_number: [
                    "D" + str(adajacent_land_number) for adajacent_land_number in adjacencies
                ] for land_number, adjacencies in json.load(adjacency_file).items()
            }
        for land_number in board_dict:
            new_land = Land()
            new_land.number = land_number
            new_land.id = new_land.board + new_land.number

            # Hardcode coastal lands
            if new_land.number in ["1", "2", "3"]:
                new_land.is_coastal = True

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

    def create_terror_handler(self):
        """Create an instance of the TerrorHandler."""
        terror_handler_args = {"n_players": self.n_players}
        self.terror_handler = TerrorHandler(terror_handler_args)

    def get_city_count_island(self) -> int:
        """Return the total city count on the island."""
        island_city_count = sum(len(land.cities) for land in self.lands)

        return island_city_count

    def get_town_count_island(self) -> int:
        """Return the total town count on the island."""
        island_town_count = sum(len(land.towns) for land in self.lands)

        return island_town_count

    def get_explorer_count_island(self) -> int:
        """Return the total explorer count on the island."""
        island_explorer_count = sum(len(land.explorers) for land in self.lands)

        return island_explorer_count

    def are_lands_adjacent(self, land, other_land):
        return other_land.id in self.adjacency_dict[land.id]
    
    def get_lands_adjacent_to_land(self, land):
        return [other for other in self.lands if self.are_lands_adjacent(land, other)]
    
    def gather_to_land(self, thing_to_gather, land: Land):
        """        
        :param thing_to_gather: the piece to gather
        :param land: the land to gather to

        Beware, this does no validation that the piece can be gathered.
        """
        self.remove(thing_to_gather)
        if isinstance(thing_to_gather, Dahan):
            land.dahan.append(thing_to_gather)
        elif isinstance(thing_to_gather, Blight):
            land.blight.append(thing_to_gather)
        elif isinstance(thing_to_gather, Explorer):
            land.explorers.append(thing_to_gather)
        elif isinstance(thing_to_gather, Town):
            land.towns.append(thing_to_gather)
        elif isinstance(thing_to_gather, City):
            land.cities.append(thing_to_gather)
        else:
            raise ValueError(f"Unexpected thing to gather: {thing_to_gather}")
            
    def remove(self, thing) -> Land:
        """
        :param thing: the piece to remove
        Remove a piece (dahan, explorer, town, city) from the island
        without having to know what land it's in. Returns the land it was removed from.
        """
        for land in self.lands:
            if thing in land.dahan:
                land.dahan.remove(thing)
                return land
            elif thing in land.blight:
                land.blight.remove(thing)
                return land
            elif thing in land.explorers:
                land.explorers.remove(thing)
                return land
            elif thing in land.towns:
                land.towns.remove(thing)
                return land
            elif thing in land.cities:
                land.cities.remove(thing)
                return land
        raise ValueError(f"Could not find thing to remove: {thing}")