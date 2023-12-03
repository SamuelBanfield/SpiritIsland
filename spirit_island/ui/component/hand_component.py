import pygame
import os

from spirit_island.framework.power_cards.power_card_base import SpiritPower  
from spirit_island.framework.island import Island

from spirit_island.ui.util import SPIRIT_BOARD_BACKGROUND
from spirit_island.ui.component.component import UIComponent

from spirit_island.framework.power_cards.shadows_flicker_like_flame import crops_wither_and_fade

from typing import Tuple


class HandComponent(UIComponent):
    def __init__(
        self, width: int, height: int, topleft: Tuple[int, int], island: Island, worker_thread_executor
    ):
        super().__init__()
        self._surface: pygame.surface.Surface = pygame.surface.Surface((width, height))
        self._rect = pygame.rect.Rect(topleft, (width, height))
        self._width, self._height = width, height
        self._island = island
        self._cards = [
            PowerCardUI(
                crops_wither_and_fade,
                self._height,
                island,
                worker_thread_executor
            )
        ]

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        self._surface.fill(SPIRIT_BOARD_BACKGROUND)
        self._surface.fill((255, 0, 0))
        for card in self._cards:
            card.render(self._surface, False)
        dest.blit(self._surface, self._rect)

    def handle_click(self, click_location):
        click_location_on_component = (
            click_location[0] - self._rect.topleft[0],
            click_location[1] - self._rect.topleft[1],
        )
        for card in self._cards:
            if card.is_location_on_component(click_location_on_component):
                card.handle_click(click_location_on_component)
                return True
        return False

    def is_location_on_component(self, location) -> bool:
        return self._rect.collidepoint(location)

class PowerCardUI(UIComponent):

    def __init__(self, power_card: SpiritPower, height, island: Island, worker_thread_executor):
        """
        :param power_card: the back end power card
        """
        self._card = power_card
        self._island = island
        image_path = os.path.relpath(__file__ + "/../../../resources/images/power_cards/uniques/crops_wither_and_fade.png")
        original_image = pygame.image.load(image_path)
        self._surface = pygame.transform.scale_by(
            original_image,
            height / original_image.get_height(),
        )
        self._rect = self._surface.get_rect()
        self._worker_thread_executor = worker_thread_executor

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        dest.blit(self._surface, self._rect)

    def handle_click(self, click_location):
        self._worker_thread_executor(self._card.execute, {}, self._island)

    def is_location_on_component(self, location) -> bool:
        return self._rect.collidepoint(location)