import os

import pygame

from spirit_island.decks.invader_card import InvaderCard
from spirit_island.framework.island import Island
from spirit_island.ui.component.component import UIComponent
from spirit_island.ui.util import BLACK, FONT_SUPPLIER, SPIRIT_BOARD_BACKGROUND

image_folder = os.path.relpath(__file__ + "/../../../resources/images/invader_cards")

INVADER_CARD_ASPECT_RATIO = 0.6590909090909091  # Card width / card height


class _InvaderCardImageSupplier:
    """Caching supplier of invader card images"""

    def __init__(self) -> None:
        self._images = {}

    def get_image(self, card: InvaderCard) -> pygame.surface.Surface:
        """Get the cached image of the invader card, or load if necessary"""
        if card in self._images:
            return self._images[card]
        card_name = f"{'_'.join(card.terrains)}" + f"_{card.stage}"
        image = pygame.image.load(f"{image_folder}/{card_name}.png")
        self._images[card] = image
        return image


class InvaderTrack(UIComponent):
    """Information about invader cards"""

    def __init__(self, island: Island, height: int, topleft):
        """Fixed aspect ratio, so only height can be specified, then call get_width"""
        self._height = height
        self._island: Island = island
        self._image_supplier: _InvaderCardImageSupplier = _InvaderCardImageSupplier()

        self._font = FONT_SUPPLIER.get_font_size(16)
        self._margin = 10  # The width of the margin above the cards, between the cards and between text and cards
        self._text_height = self._font.render(
            "Placeholder", True, BLACK
        ).get_height()  # Estimate for how tall the text will be
        self._card_height = self._height - (3 * self._margin + self._text_height)
        self._card_width = self._card_height * INVADER_CARD_ASPECT_RATIO
        self._surface: pygame.surface.Surface = pygame.surface.Surface(
            (self.get_width(), height)
        )
        self._rect: pygame.rect.Rect = self._surface.get_rect()
        self._rect.topleft = topleft

    def get_width(self):
        return self._card_width * 3 + self._margin * 4

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        """Render the current invader cards"""
        self._surface.fill(SPIRIT_BOARD_BACKGROUND)

        for index, stage in enumerate(["ravage", "build", "explore"]):
            # Create and blit the stage name above the card
            capitalised_stage_name = stage[0].upper() + stage[1:]
            stage_name_image = self._font.render(capitalised_stage_name, True, BLACK)
            stage_name_rect = stage_name_image.get_rect()
            # Center the stage name with the card below it
            stage_name_rect.center = (
                self._margin * (index + 1) + self._card_width * (index + 0.5),
                self._margin + self._text_height / 2,
            )
            self._surface.blit(stage_name_image, stage_name_rect)

            # If the card is present, also blit its image
            if self._island.invader_track[stage]:
                card = self._image_supplier.get_image(self._island.invader_track[stage])
                rect = pygame.rect.Rect(
                    (
                        self._margin + index * (self._card_width + self._margin),
                        self._margin * 2 + self._text_height,
                    ),
                    (self._card_width, self._card_height),
                )
                self._surface.blit(
                    pygame.transform.scale(card, (self._card_width, self._card_height)),
                    rect,
                )

        dest.blit(self._surface, self._rect)

    def handle_click(self, click_location):
        return

    def is_location_on_component(self, location) -> bool:
        return self._rect.collidepoint(location)
