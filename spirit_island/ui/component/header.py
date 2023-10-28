import os

import pygame

from spirit_island.decks.invader_card import InvaderCard
from spirit_island.framework.island import Island
from spirit_island.ui.util import BLACK, FONT_SUPPLIER, SPIRIT_BOARD_BACKGROUND

image_folder = os.path.relpath(__file__ + "/../../../resources/images/invader_cards")

jungle_1_image = pygame.image.load(image_folder + "/jungle_1.png")
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


class Header:
    """The header at the top of the board containing information about invader cards, fear cards etc"""

    def __init__(self, island: Island, width: int, height: int):
        self._surface: pygame.surface.Surface = pygame.surface.Surface((width, height))
        self._width = width
        self._height = height
        self._island: Island = island
        self._rect: pygame.rect.Rect = self._surface.get_rect()
        self._image_supplier: _InvaderCardImageSupplier = _InvaderCardImageSupplier()

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        """Render the current invader cards"""
        self._surface.fill(SPIRIT_BOARD_BACKGROUND)

        font = FONT_SUPPLIER.get_font_size(16)

        margin = 10  # The width of the margin above the cards, between the cards and between text and cards
        text_height = font.render(
            "Placeholder", True, BLACK
        ).get_height()  # Estimate for how tall the text will be
        card_height = self._height - (3 * margin + text_height)
        card_width = card_height * INVADER_CARD_ASPECT_RATIO

        for index, stage in enumerate(["ravage", "build", "explore"]):
            # Create and blit the stage name above the card
            capitalised_stage_name = stage[0].upper() + stage[1:]
            stage_name_image = font.render(capitalised_stage_name, True, BLACK)
            stage_name_rect = stage_name_image.get_rect()
            # Center the stage name with the card below it
            stage_name_rect.center = (
                margin * (index + 1) + card_width * (index + 0.5),
                margin + text_height / 2,
            )
            self._surface.blit(stage_name_image, stage_name_rect)

            # If the card is present, also blit its image
            if self._island.invader_track[stage]:
                card = self._image_supplier.get_image(self._island.invader_track[stage])
                rect = pygame.rect.Rect(
                    (margin + index * (card_width + margin), margin * 2 + text_height),
                    (card_width, card_height),
                )
                self._surface.blit(
                    pygame.transform.scale(card, (card_width, card_height)), rect
                )

        dest.blit(self._surface, self._rect)

    def handle_click(self, click_location):
        return

    def is_location_on_component(self, location) -> bool:
        return self._rect.collidepoint(location)
