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
        test_island.terror_handler.fear_capacity = 4
        test_island.terror_handler.fear_earned = 1

        test_island.terror_handler.add_fear(2)

        actual_fear_generated = test_island.terror_handler.fear_earned
        actual_fear_cards = test_island.terror_handler.fear_cards_pending

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
        test_island.terror_handler.terror_level = 1
        test_island.terror_handler.fear_cards_to_next_level = 3
        test_island.terror_handler.fear_capacity = 4
        test_island.terror_handler.fear_earned = 3

        test_island.terror_handler.add_fear(2)

        actual_fear_generated = test_island.terror_handler.fear_earned
        actual_fear_cards = test_island.terror_handler.fear_cards_pending
        actual_terror_level = test_island.terror_handler.terror_level

        expected_fear_generated = 1
        expected_fear_cards = 1
        expected_terror_level = 1

        assert (
            actual_fear_generated == expected_fear_generated
        ), f"Expected {expected_fear_generated} fear in pool, there was actually {actual_fear_generated}"

        assert (
            actual_fear_cards == expected_fear_cards
        ), f"Expected {expected_fear_cards} fear cards, there were actually {actual_fear_cards}"

        assert (
            actual_terror_level == expected_terror_level
        ), f"Expected Terror Level {expected_terror_level}, it is actually Terror Level {actual_terror_level}"

    def test_fear_generation_next_terror_level(self):
        """Test the island's generate_fear method with a fear card + terror level increase."""
        test_island = copy.deepcopy(self.runner.island)
        test_island.terror_handler.terror_level = 1
        test_island.terror_handler.fear_cards_to_next_level = 1
        test_island.terror_handler.fear_capacity = 4
        test_island.terror_handler.fear_earned = 3

        test_island.terror_handler.add_fear(2)

        actual_fear_generated = test_island.terror_handler.fear_earned
        actual_fear_cards = test_island.terror_handler.fear_cards_pending
        actual_terror_level = test_island.terror_handler.terror_level

        expected_fear_generated = 1
        expected_fear_cards = 1
        expected_terror_level = 2

        assert (
            actual_fear_generated == expected_fear_generated
        ), f"Expected {expected_fear_generated} fear in pool, there was actually {actual_fear_generated}"

        assert (
            actual_fear_cards == expected_fear_cards
        ), f"Expected {expected_fear_cards} fear cards, there were actually {actual_fear_cards}"

        assert (
            actual_terror_level == expected_terror_level
        ), f"Expected Terror Level {expected_terror_level}, it is actually Terror Level {actual_terror_level}"
