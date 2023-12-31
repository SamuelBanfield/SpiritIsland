import copy
import os
import random
from typing import List

import pygame
from overrides import override

from spirit_island.framework.exceptions import UIException
from spirit_island.framework.input_request import InputHandler, InputRequest
from spirit_island.framework.island import Island
from spirit_island.framework.land import Land
from spirit_island.framework.logger import logger
from spirit_island.framework.pieces import *
from spirit_island.launcher import read_json
from spirit_island.ui.component.component import UIComponent
from spirit_island.ui.inside_land import is_point_inside_polygon
from spirit_island.ui.util import BLACK, SPIRIT_BOARD_BACKGROUND

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
    def __init__(self, island: Island, offset, parent_component_size, input_handler: InputHandler):
        super().__init__()
        self._island = island
        self._input_handler = input_handler
        self._offset = offset  # Where on the destination rect the top left of the board should be
        board_info_path = os.path.relpath(
            __file__ + "/../../resources/board_d_coords.json"
        )

        board_info = read_json(board_info_path)
        self._lands = [
            LandUI(
                self._input_handler,
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
        self._scale_factor = (
            max(
                parent_component_size[0] / self._board_rect.width,
                parent_component_size[1] / self._board_rect.height,
            )
            / 1.5
        )
        self.board_topleft = [0, 0]

    @override
    def render(self, dest: pygame.surface.Surface, hovered: bool):
        self._board_surf.fill(SPIRIT_BOARD_BACKGROUND)
        self._board_surf.blit(BOARD_IMAGE, self._board_rect)
        hovered_land = self.get_land_at_location(pygame.mouse.get_pos())
        for land in self._lands:
            land.render(self._board_surf, land == hovered_land)

        scaled_image = pygame.transform.scale_by(self._board_surf, self._scale_factor)
        dest.blit(
            scaled_image,
            pygame.rect.Rect(
                self._offset, (scaled_image.get_width(), scaled_image.get_height())
            ),
        )

    @override
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self._offset[0] += 10
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self._offset[0] -= 10
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self._offset[1] += 10
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self._offset[1] -= 10

    @override
    def handle_click(self, click_location):
        if selected_land := self.get_land_at_location(click_location):
            selected_land.handle_click(self.scale_location(click_location))

    def scale_location(self, location):
        return (
            (location[0] - self._offset[0]) // self._scale_factor,
            (location[1] - self._offset[1]) // self._scale_factor,
        )

    def get_land_at_location(self, parent_coords):
        """Return the land that the point is inside, else None"""
        for land in self._lands:
            if land.is_location_on_component(
                self.scale_location(parent_coords)
            ):
                return land
        return None

    def is_location_on_component(self, click_location):
        return self.get_land_at_location(click_location) is not None


class LandUI:
    def __init__(
        self, input_handler: InputHandler, land: Land, polygon: List[List[int]], locations: List[List[int]]
    ):
        self._input_handler = input_handler
        self._land = land
        self._polygon = polygon
        self._locations = locations

        self.available_locations = copy.copy(self._locations)
        self.piece_ids = []
        self.piece_uis: List[PieceUI] = []
        self.ui_waiting_list = []

    def create_piece_uis(self):
        """Create the UI of the pieces that have been added to the land"""

        pieces = (
            self._land.cities
            + self._land.towns
            + self._land.explorers
            + self._land.blight
            + self._land.dahan
        )

        for next_piece in pieces:
            if next_piece.id not in self.piece_ids:
                if len(self.available_locations) == 0:
                    logger.warning(
                        f"Could not add {next_piece.type} to land {self._land.id}: no available UI locations."
                    )
                    self.piece_ids.append(next_piece.id)
                    self.ui_waiting_list.append(next_piece)
                else:
                    self.piece_uis.append(
                        PieceUI(self._input_handler, next_piece, self.available_locations.pop(-1))
                    )
                    self.piece_ids.append(next_piece.id)
            else:
                if (
                    next_piece in self.ui_waiting_list
                    and len(self.available_locations) > 0
                ):
                    self.piece_uis.append(
                        PieceUI(self._input_handler, next_piece, self.available_locations.pop(-1))
                    )

    def remove_piece_uis(self):
        """Find and remove the UI of the pieces that are no longer in the land"""

        pieces = (
            self._land.cities
            + self._land.towns
            + self._land.explorers
            + self._land.blight
            + self._land.dahan
        )

        for piece_id in self.piece_ids:
            id_present = False
            for next_piece in pieces:
                if piece_id == next_piece.id:
                    id_present = True
                    break
            if not id_present:
                location = self.piece_uis[self.piece_uis.index(piece_id)].piece_location
                self.piece_ids.remove(piece_id)
                self.piece_uis.remove(piece_id)  # Looks wrong
                self.available_locations.append(location)

    @override
    def render(self, dest: pygame.surface.Surface, hovered: bool):
        if hovered:
            pygame.draw.polygon(dest, BLACK, self._polygon, 6)
        self.remove_piece_uis()
        self.create_piece_uis()

        for piece_ui in self.piece_uis:
            piece_ui.render(dest, False)

    @override
    def handle_click(self, click_location):
        if input_request := self._input_handler.input_request:
            if self._land in input_request.options:
                """First check whether the selection was for the land itself"""
                logger.info(f"Selecting land '{self._land.id}' in response to: {input_request.message}")
                self._input_handler.input_request.resolution["result"] = self._land
            else:
                for piece_ui in self.piece_uis:
                    """If not, check whether the click was on a piece"""
                    if piece_ui.is_location_on_component(click_location):
                        piece_ui.handle_click(click_location)
                        return

    @override
    def is_location_on_component(self, location) -> bool:
        return is_point_inside_polygon(self._polygon, location)


class PieceUI:
    def __init__(self, input_handler: InputHandler, piece: Piece, location: list[int]):
        self._input_handler = input_handler
        self._piece = piece
        self.piece_location = location
        self.image_width = 50
        self.rect = pygame.rect.Rect(
            self.piece_location[0], self.piece_location[1], self.image_width, self.image_width
        )

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
            logger.error(f"Piece of type {self._piece.type} does not have an image.")
            raise UIException(
                f"Piece of type {self._piece.type} does not have an image."
            )

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        dest.blit(
            pygame.transform.scale(self.image, (self.image_width, self.image_width)),
            self.rect,
        )

    def handle_click(self, click_location):
        if input_request := self._input_handler.input_request:
            if self._piece in input_request.options:
                logger.info(f"Selecting piece '{self._piece.id}' in response to: {input_request.message}")
                input_request.resolution["result"] = self._piece

    def is_location_on_component(self, location) -> bool:
        return self.rect.collidepoint(location)
