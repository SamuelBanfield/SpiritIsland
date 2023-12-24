from typing import List
from spirit_island.ui.component.component import UIComponent
from spirit_island.ui.component.button import TextButton
from spirit_island.ui.util import SPIRIT_BOARD_BACKGROUND, BLACK

import pygame


class ButtonArray(UIComponent):
    def __init__(self, buttons: List[TextButton], top_left, width, height):
        self.buttons = buttons
        self.top_left = top_left
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(top_left, (width, height))
        self.margin = 10

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        self.image.fill(SPIRIT_BOARD_BACKGROUND)
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 2, border_radius=5)
        cummulative_height = self.margin
        for button in self.buttons:
            button._offset = [self.margin, cummulative_height]
            cummulative_height += button._font_rect.height + self.margin
            button.render(self.image, button.is_location_on_component(self.to_relative_coords(pygame.mouse.get_pos())))
        dest.blit(self.image, self.rect)
        
    def to_relative_coords(self, coords):
        return (coords[0] - self.top_left[0], coords[1] - self.top_left[1])

    def handle_click(self, click_location):
        relative_coords = self.to_relative_coords(click_location)
        for button in self.buttons:
            if button.is_location_on_component(relative_coords):
                button.handle_click(relative_coords)

    def is_location_on_component(self, location) -> bool:
        return self.rect.collidepoint(location)

