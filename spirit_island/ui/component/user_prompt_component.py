import pygame

from spirit_island.ui.component.component import UIComponent
from spirit_island.ui.util import SPIRIT_BOARD_BACKGROUND, FONT_SUPPLIER, BLACK


class UserPromptComponent(UIComponent):

    def __init__(self, topleft, width, height, runner):
        self.topleft = topleft
        self.width = width
        self.height = height
        self._runner = runner
        self._font = FONT_SUPPLIER.get_font_size(16)

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        text = self._runner.get_input_request().message if self._runner.get_input_request() else ""
        text_image = self._font.render(text, True, BLACK, SPIRIT_BOARD_BACKGROUND)
        rect = text_image.get_rect()
        rect.center = (self.topleft[0] + self.width // 2, self.topleft[1] + self.height // 2)
        dest.blit(text_image, rect)

    def handle_click(self, click_location):
        pass

    def is_location_on_component(self, location) -> bool:
        pass
