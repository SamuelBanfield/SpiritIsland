import os
import random
from typing import List
from overrides import override
import copy

import pygame

from spirit_island.framework.island import Island
from spirit_island.framework.land import Land
from spirit_island.framework.pieces import *
from spirit_island.launcher import read_json
from spirit_island.ui.component.component import UIComponent
from spirit_island.ui.util import SPIRIT_BOARD_BACKGROUND

image_folder = os.path.relpath(__file__ + "/../../resources/images")

blight_image = pygame.image.load(image_folder + "/blight.png")
explorer_image = pygame.image.load(image_folder + "/explorer.png")
town_image = pygame.image.load(image_folder + "/town.png")
city_image = pygame.image.load(image_folder + "/city.png")
dahan_image = pygame.image.load(image_folder + "/dahan.png")

images = [blight_image, explorer_image, town_image, city_image, dahan_image]


# Hard code board for now
rel_path = os.path.relpath(__file__ + "/../../resources/board_d.png")
BOARD_IMAGE = pygame.image.load(rel_path)


class BoardComponent(UIComponent):
    def __init__(self, island: Island, offset):
        super().__init__()
        self._island = island
        self._offset = offset # Where on the destination rect the top left of the board should be
        board_info_path = os.path.relpath(
            __file__ + "/../../resources/board_d_coords.json"
        )

        board_info = read_json(board_info_path)
        self._lands = [
            LandUI(
                land,
                board_info[land.number]["polygon"],
                board_info[land.number]["locations"],
            )
            for land in self._island.lands
        ]
        self._board_rect = BOARD_IMAGE.get_rect()
        self._board_surf = pygame.surface.Surface(
            (self._board_rect.width, self._board_rect.height)
        )

    @override
    def render(self, dest: pygame.surface.Surface, hovered: bool):
        self._board_surf.fill(SPIRIT_BOARD_BACKGROUND)
        self._board_surf.blit(BOARD_IMAGE, self._board_rect)
        for land in self._lands:
            land.render(self._board_surf, False)

        scale_factor = max(
            dest.get_width() / self._board_rect.width,
            dest.get_height() / self._board_rect.height,
        ) / 1.5
        
        scaled_image = pygame.transform.scale_by(self._board_surf, scale_factor)
        dest.blit(
            scaled_image,
            pygame.rect.Rect(self._offset, (scaled_image.get_width(), scaled_image.get_height()))
        )


class LandUI:
    def __init__(
        self, land: Land, polygon: List[List[int]], locations: List[List[int]]
    ):
        self._land = land
        self._polygon = polygon
        self._locations = locations

        self.available_locations = copy.copy(self._locations)
        self.piece_ids = []
        self.piece_uis = []

    def create_piece_uis(self):
        """Create the UI of the pieces that have been added to the land"""

        pieces = self._land.cities + self._land.towns + self._land.explorers + self._land.blight + self._land.dahan

        if len(pieces) > len(self._locations):
            print("ERROR: Not enough room to fit everything")
            return

        for next_piece in pieces:
            if next_piece.id not in self.piece_ids:
                self.piece_uis.append(PieceUI(next_piece, self.available_locations.pop(-1)))
                self.piece_ids.append(next_piece.id)

    def remove_piece_uis(self):
        """Find and remove the UI of the pieces that are no longer in the land"""

        pieces = self._land.cities + self._land.towns + self._land.explorers + self._land.blight + self._land.dahan

        for piece_id in self.piece_ids:
            id_present = False
            for next_piece in pieces:
                if piece_id == next_piece.id:
                    id_present = True
                    break
            if not id_present:
                location = self.piece_uis[self.piece_uis.index(piece_id)].piece_location
                self.piece_ids.remove(piece_id)
                self.piece_uis.remove(piece_id)
                self.available_locations.append(location)

    @override
    def render(self, dest: pygame.surface.Surface, hovered: bool):

        self.remove_piece_uis()
        self.create_piece_uis()

        for piece_ui in self.piece_uis:
            piece_ui.render(dest, False)

    @override
    def handle_click(self, click_location):
        pass

    @override
    def is_location_on_component(self, location) -> bool:
        pass


class PieceUI:
    def __init__(
        self, piece: Piece, location: list[int]
    ):
        self._piece = piece
        self.piece_location = location

        self.image = []
        self.get_image()

    def __eq__(self, other):
        return self._piece.id == other

    def get_image(self):
        if isinstance(self._piece, City):
            self.image = city_image
        elif isinstance(self._piece, Town):
            self.image = town_image
        elif isinstance(self._piece, Explorer):
            self.image = explorer_image
        elif isinstance(self._piece, Dahan):
            self.image = dahan_image
        elif isinstance(self._piece, Blight):
            self.image = blight_image
        else:
            print("Piece is not of the correct instance and so could not receive image")

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        dest.blit(
            pygame.transform.scale(self.image, (50, 50)),
            (self.piece_location[0], self.piece_location[1], 50, 50),
        )

    def handle_click(self, click_location):
        pass

    def is_location_on_component(self, location) -> bool:
        pass
