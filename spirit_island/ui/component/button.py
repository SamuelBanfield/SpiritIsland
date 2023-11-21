from typing import Callable

import pygame
from overrides import override

from spirit_island.ui.component.component import UIComponent
from spirit_island.ui.util import BLACK, FONT_SUPPLIER, GREY, WHITE


class TextButton(UIComponent):
    def __init__(
        self, text_or_provider: str | Callable, callback: Callable = None, offset=[0, 0], enablement = lambda: True, font_size: int = 24
    ):
        """
        :param text_or_provider: either the text if this button always has
        the same text, or a callback returning the button text
        :param callback: the callback called when the button is pressed
        :param offset: top left of the button on its parent surface
        :param enablement: when this button should detect clicks (so the UI
        can display that the button won't do anything). Defaults to always
        :param font_size: size of the font
        """
        super().__init__()
        self._callback = callback
        self._font = FONT_SUPPLIER.get_font_size(font_size)
        self._offset = offset
        self._is_enabled = enablement
        if isinstance(text_or_provider, str):
            self.get_text = lambda: text_or_provider
        else:
            self.get_text = text_or_provider
        self.update_text()

    def update_text(self):
        self._text = self.get_text()
        self._font_surface = self._font.render(self._text, True, BLACK, WHITE)
        self._font_surface_hover = self._font.render(self._text, True, BLACK, GREY)
        self._font_rect = self._font_surface.get_rect()
        self._font_rect.topleft = self._offset

    @override
    def render(self, dest: pygame.surface.Surface, hovered: bool):
        self.update_text()
        dest.blit(
            self._font_surface_hover if hovered and self._is_enabled() else self._font_surface, self._font_rect
        )

    @override
    def handle_click(self, click_location):
        if self._callback and self._is_enabled():
            self._callback()

    @override
    def is_location_on_component(self, location) -> bool:
        return self._font_rect.collidepoint(location)
