from overrides import override
from typing import Callable

import pygame

from spirit_island.ui.util import BLACK, GREY, WHITE
from spirit_island.ui.component.component import UIComponent

_FONTS = {}  # Cache fonts, although I'm not sure how expensive they actually are


class TextButton(UIComponent):
    def __init__(
        self, text: str, callback: Callable = None, offset=[0, 0], font_size: int = 24
    ):
        super().__init__()
        self._callback = callback
        if font_size in _FONTS:
            self._font = _FONTS[font_size]
        else:
            font = pygame.font.Font(pygame.font.get_default_font(), font_size)
            _FONTS[font_size] = font
            self._font = font
        self._offset = offset
        self.set_text(text)

    def set_text(self, text: str):
        self._text = text
        self._font_surface = self._font.render(self._text, True, BLACK, WHITE)
        self._font_surface_hover = self._font.render(self._text, True, BLACK, GREY)
        self._font_rect = self._font_surface.get_rect()
        self._font_rect.topleft = self._offset

    @override
    def render(self, dest: pygame.surface.Surface, hovered: bool):
        dest.blit(
            self._font_surface_hover if hovered else self._font_surface, self._font_rect
        )

    @override
    def handle_click(self, click_location):
        if self._callback:
            self._callback()

    @override
    def is_location_on_component(self, location) -> bool:
        return self._font_rect.collidepoint(location)
