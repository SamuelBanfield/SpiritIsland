import os
import random
from typing import List
from overrides import override

import pygame

from spirit_island.framework.island import Island
from spirit_island.framework.land import Land
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


    @override
    def render(self, dest: pygame.surface.Surface, hovered: bool):
        to_draw = (
            [dahan_image] * self._land.dahan_count
            + [explorer_image] * self._land.invader_count["explorer"]
            + [town_image] * self._land.invader_count["town"]
            + [city_image] * self._land.invader_count["city"]
            + [blight_image] * self._land.blight_count
        )

        if len(to_draw) > len(self._locations):
            print("ERROR: Not enough room to draw everything")
            return

        for i in range(len(to_draw)):
            location = self._locations[i]
            dest.blit(
                pygame.transform.scale(to_draw[i], (50, 50)),
                (location[0], location[1], 50, 50),
            )

    @override
    def handle_click(self, click_location):
        pass

    @override
    def is_location_on_component(self, location) -> bool:
        pass
