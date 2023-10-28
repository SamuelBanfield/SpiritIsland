import pygame


class UIComponent:
    def __init__(self):
        pass

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        pass

    def handle_click(self, click_location):
        pass

    def is_location_on_component(self, location) -> bool:
        pass
