import copy
import os
import unittest

from spirit_island import launcher
from spirit_island.framework.island import Island


class TestTerror(unittest.TestCase):
    def setUp(self):
        """Set up for TestTerror tests."""
        controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")
        self.runner = launcher.Runner(controls_path)

        self.runner.create_island()

    def test_fear_generation_no_card(self):
        """Test the island's generate_fear method."""
        test_island = copy.deepcopy(self.runner.island)
        test_island.n_players = 1
        test_island.fear_generated = 1

        test_island.generate_fear(2)

        actual_fear_generated = test_island.fear_generated
        actual_fear_cards = test_island.fear_cards

        expected_fear_generated = 3
        expected_fear_cards = 0

        assert (
            actual_fear_generated == expected_fear_generated
        ), f"Expected {expected_fear_generated} fear in pool, there was actually {actual_fear_generated}"

        assert (
            actual_fear_cards == expected_fear_cards
        ), f"Expected {expected_fear_cards} fear cards, there were actually {actual_fear_cards}"

    def test_fear_generation_earn_card(self):
        """Test the island's generate_fear method with a fear card."""
        test_island = copy.deepcopy(self.runner.island)
        test_island.n_players = 1
        test_island.fear_generated = 3

        test_island.generate_fear(2)
        actual_fear_generated = test_island.fear_generated
        actual_fear_cards = test_island.fear_cards

        expected_fear_generated = 1
        expected_fear_cards = 1

        assert (
            actual_fear_generated == expected_fear_generated
        ), f"Expected {expected_fear_generated} fear in pool, there was actually {actual_fear_generated}"

        assert (
            actual_fear_cards == expected_fear_cards
        ), f"Expected {expected_fear_cards} fear cards, there were actually {actual_fear_cards}"
