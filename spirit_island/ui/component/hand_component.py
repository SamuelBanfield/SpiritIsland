import pygame

from spirit_island.ui.util import SPIRIT_BOARD_BACKGROUND
from spirit_island.ui.component.component import UIComponent

from typing import Tuple


class HandComponent(UIComponent):
    def __init__(
        self, width: int, height: int, topleft: Tuple[int, int]
    ):
        super().__init__()
        self._surface: pygame.surface.Surface = pygame.surface.Surface((width, height))
        self._rect = pygame.rect.Rect(topleft, (width, height))
        self._width, self._height = width, height

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        self._surface.fill(SPIRIT_BOARD_BACKGROUND)
        self._surface.fill((255, 0, 0))
        dest.blit(self._surface, self._rect)

    def handle_click(self, click_location):
        pass

    def is_location_on_component(self, location) -> bool:
        pass