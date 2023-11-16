import copy
import os
import unittest

from spirit_island import launcher
from spirit_island.test_support.input_handler import TestInputHandler
from spirit_island.framework.island import Island
from spirit_island.actions.invader_actions import RavageAction


class TestTerror(unittest.TestCase):
    def setUp(self):
        """Set up for TestTerror tests."""
        controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")
        self.runner = launcher.Runner(controls_path, TestInputHandler())

        self.runner.create_island()

    def test_fear_generation_no_card(self):
        """Test the island's generate_fear method."""
        test_island = self.runner.island
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
        test_island = self.runner.island
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
        test_island = self.runner.island
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

class TestAdjacencies(unittest.TestCase):
    def setUp(self):
        """Set up for TestTerror tests."""
        controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")
        self.runner = launcher.Runner(controls_path, TestInputHandler())

        self.runner.create_island()

    def test_adajacencies(self):
        expected_adjacencies = {
            "D0": ["D1", "D2", "D3"],
            "D1": ["D2", "D5", "D7", "D8"],
            "D2": ["D1", "D3", "D4", "D5"],
            "D3": ["D2", "D4"],
            "D4": ["D2", "D3", "D5", "D6"],
            "D5": ["D1", "D2", "D4", "D6", "D7"],
            "D6": ["D4", "D5", "D7"],
            "D7": ["D1", "D5", "D6", "D8"],
            "D8": ["D1", "D7"]
        }

        assert (
            self.runner.island.adjacency_dict == expected_adjacencies
        ), f"Unexpected adjacenceis {self.runner.island.adjacency_dict}, expected {expected_adjacencies}"

class TestBlightCascade(unittest.TestCase):

    def setUp(self):
        """Set up for blight cascade tests."""
        controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")
        self.runner = launcher.Runner(controls_path, TestInputHandler())
        self.input_handler = self.runner.input_handler
        self.runner.create_island()

    def assert_blight(self, expected_blight, actual_blight):
        """
        :param expected_blight: the expected number of blight
        :param actual_blight: that actual number of blight
        """
        assert (
            expected_blight == actual_blight
        ), f"Unexpected blight count: {actual_blight}, expected {expected_blight}"


    def test_blight_empty_land(self):
        test_controls = {
            "board": "board_d.json",
            "auto_allocate_damage": True,
        }
        island = self.runner.island
        land = island.lands[1]
        self.assert_blight(0, len(land.blight))
        island.add_blight(land)

        self.assert_blight(1, len(land.blight))

    def test_cascade(self):
        test_controls = {
            "board": "board_d.json",
            "auto_allocate_damage": True,
        }
        island = self.runner.island
        land_one = island.lands[1]
        land_two = island.lands[2]

        island.add_blight(land_one)
        self.input_handler.add_expected_request(
            selection = land_two,
            reason = "Select land for blight cascade"
        )
        island.add_blight(land_one)

        self.assert_blight(2, len(land_one.blight))
        self.assert_blight(1, len(land_two.blight))

    def test_cascade_back_to_origin_land(self):
        test_controls = {
            "board": "board_d.json",
            "auto_allocate_damage": True,
        }
        island = self.runner.island
        land_one = island.lands[1]
        land_two = island.lands[2]
        land_seven = island.lands[7]

        island.add_blight(land_one)
        island.add_blight(land_two)
        self.input_handler.add_expected_request(
            selection = land_two,
            reason = "Select land for blight cascade"
        )
        self.input_handler.add_expected_request(
            selection = land_one,
            reason = "Select land for blight cascade"
        )
        self.input_handler.add_expected_request(
            selection = land_seven,
            reason = "Select land for blight cascade"
        )
        island.add_blight(land_one)

        self.assert_blight(3, len(land_one.blight))
        self.assert_blight(2, len(land_two.blight))
        self.assert_blight(1, len(land_seven.blight))
