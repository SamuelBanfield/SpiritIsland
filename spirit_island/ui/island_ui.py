import os
import pygame

from typing import List

from spirit_island.framework.island import Island
from spirit_island.framework.land import Land
from spirit_island.launcher import read_json

class IslandUI:

    def __init__(self, island: Island):
        self._island = island
        board_info_path = os.path.relpath(__file__ + "/../../resources/board_d_coords.json")
        
        board_info = read_json(board_info_path)
        self._lands = [LandUI(land, board_info[land.number]["polygon"], board_info[land.number]["locations"]) for land in self._island.lands]

    def draw(self, dest: pygame.surface.Surface):
        for land in self._lands:
            land.draw(dest)

class LandUI:

    def __init__(self, land: Land, polygon: List[List[int]], locations: List[List[int]]):
        self._land = land
        self._polygon = polygon
        self._locations = locations

    def draw(self, dest: pygame.surface.Surface):
        for location in self._locations:
            pygame.draw.rect(dest, (255, 0, 0), (location[0], location[1], 40, 40))
