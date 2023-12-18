import os

import pygame

from spirit_island.decks.invader_card import InvaderCard
from spirit_island.framework.island import Island
from spirit_island.ui.component.component import UIComponent
from spirit_island.ui.component.fear_component import FearComponent
from spirit_island.ui.component.invader_track import InvaderTrack
from spirit_island.ui.component.user_prompt_component import UserPromptComponent
from spirit_island.ui.util import BLACK, FONT_SUPPLIER, SPIRIT_BOARD_BACKGROUND


class Header(UIComponent):
    """The header at the top of the board containing information about invader cards, fear cards etc"""

    def __init__(self, island: Island, width: int, height: int, runner):
        self._surface: pygame.surface.Surface = pygame.surface.Surface((width, height))
        self._width = width
        self._height = height
        self._rect: pygame.rect.Rect = self._surface.get_rect()
        invader_track = InvaderTrack(island, height, (0, 0))
        fear_component = FearComponent(
            island, height, height, (invader_track.get_width(), 0)
        )
        user_prompt_component = UserPromptComponent((invader_track.get_width() + height, 0), width - invader_track.get_width() - height, height, runner)
        self._components = [invader_track, fear_component, user_prompt_component]

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        """Render the current invader cards"""
        self._surface.fill(SPIRIT_BOARD_BACKGROUND)
        for component in self._components:
            component.render(self._surface, hovered)
        pygame.draw.line(self._surface, BLACK, (0, self._height - 2), (self._width, self._height - 2), 2)
        dest.blit(self._surface, self._rect)

    def handle_click(self, click_location):
        return

    def is_location_on_component(self, location) -> bool:
        return self._rect.collidepoint(location)
