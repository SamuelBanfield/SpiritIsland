import os

import pygame

from spirit_island.framework.island import Island
from spirit_island.launcher import Runner
from spirit_island.ui.component.button import TextButton
from spirit_island.ui.component.header import Header
from spirit_island.ui.island_ui import BoardComponent
from spirit_island.ui.util import SPIRIT_BOARD_BACKGROUND

pygame.init()


class UI:
    def __init__(self, island: Island, options={}):
        self.options = {"FPS": 60, "WIDTH": 1200, "HEIGHT": 800}
        for option in options:
            self.options[option] = options[option]
        self._runner = Runner()
        self._runner.create_island()
        self._runner.create_phases()
        header_height = self.options["HEIGHT"] // 5
        self._island_ui = BoardComponent(self._runner.island, (0, header_height))
        self.header = Header(self._runner.island, self.options["WIDTH"], header_height)

        # Next phase button
        next_phase_button = TextButton(
            "Next phase",
            self._runner.perform_phase,
            offset=[0, self.options["WIDTH"] // 4],
        )
        self._current_phase_image = TextButton("", offset=[0, header_height])
        self._components = [
            self._island_ui,
            next_phase_button,
            self._current_phase_image,
            self.header,
        ]

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
        dest.fill(SPIRIT_BOARD_BACKGROUND)
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
