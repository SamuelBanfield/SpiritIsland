import json
import sys

import pygame
from pygame.time import Clock

pygame.init()


FPS = 60
WIDTH = 1000
HEIGHT = 800
CARDS_IMAGE = pygame.image.load("./spirit_island/resources/images/invader_cards_scaled.png")

def add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

class CardViewer:
    def __init__(self):
        self.clock = Clock()
        self.offset = [-190, -3]
        self.cards = []
        self.card_num = 0

    def run(self):
        display = pygame.display.set_mode((WIDTH, HEIGHT))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_button_up()
                if event.type == pygame.KEYUP:
                    self.key_up(event.key)
            self.render(display)
            pygame.display.flip()
            self.clock.tick(FPS)

    def render(self, display):
        display.fill((0, 0, 0))
        rect = CARDS_IMAGE.get_rect()
        rect.topleft = self.offset
        display.blit(CARDS_IMAGE, rect)
        # width = 261
        # height = 396
        # topleft = (190, 3)

    def mouse_button_up(self):
        # No-op for override
        pass

    def key_up(self, key):
        # No-op for override
        width = 261
        height = 396
        # topleft = (190, 3)
        surf = pygame.surface.Surface((width, height))
        rect = CARDS_IMAGE.get_rect()
        rect.topleft = self.offset
        surf.blit(CARDS_IMAGE, rect)
        if key == pygame.K_p:
            pygame.image.save(surf, f"file_{self.card_num}")
            self.card_num += 1
            print("Saved")
        elif key == pygame.K_w:
            self.offset[1] += 396
        elif key == pygame.K_s:
            self.offset[1] -= 396
        elif key == pygame.K_a:
            self.offset[0] += 261
        elif key == pygame.K_d:
            self.offset[0] -= 261

if __name__ == "__main__":
    CardViewer().run()