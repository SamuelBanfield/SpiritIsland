import os

import pygame

from spirit_island.framework.island import Island
from spirit_island.launcher import Runner
from spirit_island.ui.component.button import TextButton
from spirit_island.ui.island_ui import IslandUI

pygame.init()

# Hard code board for now
rel_path = os.path.relpath(__file__ + "/../../resources/board_d.png")
BOARD_IMAGE = pygame.image.load(rel_path)


class UI:
    def __init__(self, island: Island, options={}):
        self.options = {"FPS": 60, "WIDTH": 1200, "HEIGHT": 800}
        for option in options:
            self.options[option] = options[option]
        self._runner = Runner()
        self._runner.create_island()
        self._runner.create_phases()
        self._island_ui = IslandUI(self._runner.island)

        # Board image
        self.board_rect = BOARD_IMAGE.get_rect()
        self.board_surf = pygame.surface.Surface(
            (self.board_rect.width, self.board_rect.height)
        )
        self.board_surf.blit(BOARD_IMAGE, self.board_rect)

        # Next phase button
        next_phase_button = TextButton("Next phase", self._runner.perform_phase)
        self._current_phase_image = TextButton("", offset=[0, 50])
        self._components = [next_phase_button, self._current_phase_image]

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for child in self._components:
                if child.is_location_on_component(mouse_pos):
                    child.handle_click(mouse_pos)

    def render(self, dest: pygame.Surface):
        self.board_surf.blit(BOARD_IMAGE, self.board_rect)
        self._island_ui.draw(self.board_surf)
        scale_factor = max(
            dest.get_width() / self.board_rect.width,
            dest.get_height() / self.board_rect.height,
        )
        dest.blit(
            pygame.transform.scale_by(self.board_surf, scale_factor), self.board_rect
        )
        self._current_phase_image.set_text(self._runner.get_current_phase())
        for child in self._components:
            child.render(dest, child.is_location_on_component(pygame.mouse.get_pos()))

    def run(self):
        display = pygame.display.set_mode(
            (self.options["WIDTH"], self.options["HEIGHT"])
        )
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                self.handle_event(event)
            self.render(display)
            pygame.display.flip()
            clock.tick(self.options["FPS"])
