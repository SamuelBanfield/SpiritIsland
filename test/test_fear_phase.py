import copy
import os
import random
import unittest
from typing import List

from spirit_island import launcher
from spirit_island.decks.fear_cards import *
from spirit_island.decks.fear_deck_handler import FearDeckHandler
from spirit_island.framework.island import Island
from spirit_island.framework.land import Land
from spirit_island.phases.fear_card_phase import FearPhase


class TestFearPhase(unittest.TestCase):
    def setUp(self):

        controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")
        self.runner = launcher.Runner(controls_path)

        self.runner.create_island()
        self.runner.create_phases()

    def test_construct_fear_deck(self):
        fear_phase: FearPhase = copy.deepcopy(self.runner.fear_card_phase)
        # Expected fear deck is base fear deck from fear_deck_handler.py
        expected_fear_deck = {
            "OverseasTrade": OverseasTrade,
        }
        actual_fear_deck = fear_phase.fear_deck_handler.fear_deck

        assert (
            actual_fear_deck == expected_fear_deck
        ), f"Fear deck {actual_fear_deck} does not match {expected_fear_deck}"

    def test_select_random_fear_card(self):
        fear_phase: FearPhase = copy.deepcopy(self.runner.fear_card_phase)
        fear_phase.fear_deck_handler.fear_deck = {
            "FearCard1": FearCardBase,
            "FearCard2": FearCardTest,
            "FearCard3": OverseasTrade,
        }
        random.seed(100)

        card1 = fear_phase.fear_deck_handler.select_random_fear_card()
        card2 = fear_phase.fear_deck_handler.select_random_fear_card()

        assert isinstance(card1, FearCardBase), f"Unexpected fear card {type(card1)}"
        assert isinstance(card2, OverseasTrade), f"Unexpected fear card {type(card2)}"

    def test_execute_fear_phase(self):
        fear_phase: FearPhase = copy.deepcopy(self.runner.fear_card_phase)

        fear_phase.island.terror_handler.fear_cards_pending = 1
        fear_phase.island.terror_handler.terror_level = 3
        fear_phase.fear_deck_handler.fear_deck = {
            "OverseasTrade": OverseasTrade,
        }

        fear_phase.begin_phase()

        assert (
            fear_phase.island.lands[1].defend == 9
        ), f"Unexpected result from OverseasTrade level 3"

    def test_move_card_to_discard(self):
        fear_phase: FearPhase = copy.deepcopy(self.runner.fear_card_phase)
        card = fear_phase.fear_deck_handler.select_random_fear_card()

        fear_phase.move_fear_card_to_discard(card)

        assert fear_phase.fear_deck_handler.fear_card_discard_pile == [
            card
        ], f"Fear card was not moved to discard pile"
