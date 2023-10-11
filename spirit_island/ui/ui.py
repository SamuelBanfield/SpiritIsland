import pygame
import os

from spirit_island.framework.island import Island

pygame.init()
rel_path = os.path.relpath(__file__ + "/../../resources/board_d.png")

BOARD_IMAGE = pygame.image.load(rel_path)

class UI:

    def __init__(self, island: Island, options = {}):
        self.__island = island
        self.options = {
            "FPS": 60,
            "WIDTH": 1200,
            "HEIGHT": 800
        }
        for option in options:
            self.options[option] = options[option]

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.get_pos()

    def render(self, dest: pygame.Surface):
        dest.fill((0, 0, 0))
        dest.blit(BOARD_IMAGE, BOARD_IMAGE.get_rect())

    def run(self):
        display = pygame.display.set_mode((self.options["WIDTH"], self.options["HEIGHT"]))
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                self.handle_event(event)
            self.render(display)
            pygame.display.flip()
            clock.tick(self.options["FPS"])
