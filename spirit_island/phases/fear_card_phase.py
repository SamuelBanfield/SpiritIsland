from spirit_island.decks.fear_cards import FearCardBase
from spirit_island.decks.fear_deck_handler import FearDeckHandler
from spirit_island.framework.island import Island
from spirit_island.phases.phases_base import Phase


class FearPhase(Phase):
    """Phase for performing pending fear cards."""

    def __init__(self, controls: dict, island: Island):
        super().__init__(controls, island, name="Fear Cards")
        # Create a fear deck handler
        self.fear_deck_handler = FearDeckHandler()

    def execute_phase(self):
        print(f"Fear Card Phase: turn {self.island.turn_counter}")
        # Check if any fear cards are pending
        while self.island.terror_handler.fear_cards_pending > 0:
            pending_cards = self.island.terror_handler.fear_cards_pending
            print(f"Pending fear cards: {pending_cards}")
            self.island.terror_handler.fear_cards_pending -= 1
            # Now perform a fear card
            current_fear_card = self.fear_deck_handler.select_random_fear_card()
            print(f"Fear card is {current_fear_card.name}")
            self.perform_fear_card(current_fear_card, self.island)
            self.move_fear_card_to_discard(current_fear_card)

        print("Fear Card Phase Complete")

    @staticmethod
    def perform_fear_card(fear_card: FearCardBase, island: Island):
        current_terror_level = island.terror_handler.terror_level
        if current_terror_level == 1:
            fear_card.level1_effect(island)
        elif current_terror_level == 2:
            fear_card.level2_effect(island)
        else:
            fear_card.level3_effect(island)

    def move_fear_card_to_discard(self, fear_card: FearCardBase):
        self.fear_deck_handler.fear_card_discard_pile.append(fear_card)
