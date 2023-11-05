import os
from typing import Tuple

import pygame

from spirit_island.framework.island import Island
from spirit_island.ui.component.component import UIComponent
from spirit_island.ui.util import BLACK, FONT_SUPPLIER, SPIRIT_BOARD_BACKGROUND

image_folder = os.path.relpath(__file__ + "/../../../resources/images/")

fear_token_image = pygame.image.load(image_folder + "/fear_token.png")
terror_level_images = {terror_level: pygame.image.load(image_folder + f"/terror_level_{terror_level}.png") for terror_level in range(1, 4)}


class FearComponent(UIComponent):
    def __init__(
        self, island: Island, width: int, height: int, topleft: Tuple[int, int]
    ):
        super().__init__()
        self._surface: pygame.surface.Surface = pygame.surface.Surface((width, height))
        self._rect = pygame.rect.Rect(topleft, (width, height))
        self._width, self._height = width, height
        self._island = island

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        self._surface.fill(SPIRIT_BOARD_BACKGROUND)

        # Draw the current terror level
        current_terror_level_image = terror_level_images[self._island.terror_level]
        terror_level_rect = current_terror_level_image.get_rect()
        terror_level_rect.center = (self._width // 2, self._height // 3)
        self._surface.blit(current_terror_level_image, terror_level_rect)

        # Draw the fear pool (e.g. "1/4")
        fear_pool_text = FONT_SUPPLIER.get_font_size(24).render(
            f"{self._island.fear_earned}/{self._island.fear_capacity}", True, BLACK
        )
        fear_pool_text_rect = fear_pool_text.get_rect()
        fear_pool_text_rect.center = (self._width // 2, 2 * self._height // 3)
        self._surface.blit(fear_pool_text, fear_pool_text_rect)
        dest.blit(self._surface, self._rect)

    def handle_click(self, click_location):
        return

    def is_location_on_component(self, location) -> bool:
        return self._rect.collidepoint(location)
