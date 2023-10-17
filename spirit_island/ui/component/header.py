import pygame

class Header:

    def __init__(self, width: int, height: int):
        self._surface = pygame.surface.Surface((width, height))
        self._rect = self._surface.get_rect()

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        dest.blit(
            self._surface, self._rect
        )

    def handle_click(self, click_location):
        return 

    def is_location_on_component(self, location) -> bool:
        return self._rect.collidepoint(location)