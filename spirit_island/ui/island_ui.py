import os
import random
from typing import List

import pygame

from spirit_island.framework.island import Island
from spirit_island.framework.land import Land
from spirit_island.launcher import read_json

image_folder = os.path.relpath(__file__ + "/../../resources/images")

blight_image = pygame.image.load(image_folder + "/blight.png")
explorer_image = pygame.image.load(image_folder + "/explorer.png")
town_image = pygame.image.load(image_folder + "/town.png")
city_image = pygame.image.load(image_folder + "/city.png")
dahan_image = pygame.image.load(image_folder + "/dahan.png")

images = [blight_image, explorer_image, town_image, city_image, dahan_image]


class IslandUI:
    def __init__(self, island: Island):
        self._island = island
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

    def draw(self, dest: pygame.surface.Surface):
        for land in self._lands:
            land.draw(dest)


class LandUI:
    def __init__(
        self, land: Land, polygon: List[List[int]], locations: List[List[int]]
    ):
        self._land = land
        self._polygon = polygon
        self._locations = locations

    def draw(self, dest: pygame.surface.Surface):
        self._land.blight_count
        to_draw = (
            [dahan_image] * self._land.dahan_count
            + [explorer_image] * self._land.invader_count["explorer"]
            + [town_image] * self._land.invader_count["town"]
            + [city_image] * self._land.invader_count["city"]
            + [blight_image] * self._land.blight_count
        )

        if len(to_draw) > len(self._locations):
            print("ERROR: Not enough room to draw everything")

        for i in range(len(to_draw)):
            location = self._locations[i]
            dest.blit(
                pygame.transform.scale(to_draw[i], (50, 50)),
                (location[0], location[1], 50, 50),
            )
