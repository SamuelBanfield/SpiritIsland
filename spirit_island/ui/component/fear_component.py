import os
import pygame

from typing import Tuple

from spirit_island.ui.component.component import UIComponent
from spirit_island.framework.island import Island
from spirit_island.ui.util import SPIRIT_BOARD_BACKGROUND, FONT_SUPPLIER, BLACK


image_folder = os.path.relpath(__file__ + "/../../../resources/images/")

fear_token_image = pygame.image.load(image_folder + "/fear_token.png")

class FearComponent(UIComponent):

    def __init__(self, island: Island, width: int, height: int, topleft: Tuple[int, int]):
        super().__init__()
        self._surface: pygame.surface.Surface = pygame.surface.Surface((width, height))
        self._rect = pygame.rect.Rect(topleft, (width, height))
        self._width, self._height = width, height
        self._island = island

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        self._surface.fill(SPIRIT_BOARD_BACKGROUND)

        fear_token_rect = fear_token_image.get_rect()
        fear_token_rect.center = (self._width // 2, self._height // 3)
        self._surface.blit(fear_token_image, fear_token_rect)

        fear_pool_text = FONT_SUPPLIER.get_font_size(24).render(f"{self._island.fear_generated}/{self._island.fear_capacity}", True, BLACK)
        fear_pool_text_rect = fear_pool_text.get_rect()
        fear_pool_text_rect.center = (self._width // 2, 2 * self._height // 3)
        self._surface.blit(fear_pool_text, fear_pool_text_rect)
        dest.blit(self._surface, self._rect)

    def handle_click(self, click_location):
        return

    def is_location_on_component(self, location) -> bool:
        return self._rect.collidepoint(location)
