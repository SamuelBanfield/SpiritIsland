import random

from spirit_island.decks.fear_cards import *


class FearDeckHandler:
    """Class for managing the fear deck. The fear card phases uses this class to perform fear cards."""

    def __init__(self):
        self.fear_deck = {}
        self.fear_card_discard_pile = []
        self.construct_fear_deck()

    def construct_fear_deck(self):
        """Assigns the fear deck to the handler. The fear deck is a dictionary of all available fear card classes."""
        base_fear_deck = {
            "OverseasTrade": OverseasTrade,
        }
        self.fear_deck = base_fear_deck

    def select_random_fear_card(self) -> FearCardBase:
        """
        Randomly selects a new fear card class and removes that class from the fear deck.
        :return: A fear card object of random class
        """
        # If the fear deck is empty then reshuffle and begin again
        if not self.fear_deck:
            self.construct_fear_deck()
            print("Fear deck was empty, so has been reshuffled")

        # Randomly select a fear card class from the available
        random_card = random.choice(list(self.fear_deck.keys()))
        selected_class = self.fear_deck.pop(random_card)
        fear_card_object = selected_class()

        return fear_card_object
