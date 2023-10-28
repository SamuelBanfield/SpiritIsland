import pygame

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SPIRIT_BOARD_BACKGROUND = (221, 203, 121)


class _FontSupplier:
    """Caching supplier of fonts"""

    def __init__(self):
        self._fonts = {}

    def get_font_size(self, font_size: int):
        """Returns a font of the specified size"""
        if font_size in self._fonts:
            return self._fonts[font_size]
        font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        self._fonts[font_size] = font
        return font


FONT_SUPPLIER = _FontSupplier()
