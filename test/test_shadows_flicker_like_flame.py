import unittest
from spirit_island.actions.invader_actions import RavageAction

from spirit_island.framework.power_cards.shadows_flicker_like_flame import concealing_shadows, crops_wither_and_fade
from spirit_island.framework.island import Island
from spirit_island.test_support.input_handler import TestInputHandler

class TestCropsWitherAndFade(unittest.TestCase):

    def setUp(self):
        test_controls = {
            "board": "single_empty_land.json",
        }
        self.input_handler = TestInputHandler()
        self.island = Island(test_controls, self.input_handler)
        self.land = self.island.lands[0]

        self.input_handler.add_expected_request(
            self.land,
            reason="Select target land for crops wither and fade"
        )

    def test_crops_wither_and_fade_town(self):
        self.island.add_piece("town", self.land)
        self.input_handler.add_expected_request(
            self.land.towns[0],
            reason="Select town or city to downgrade"
        )
        
        crops_wither_and_fade.execute({}, self.island)

        assert (
            self.island.terror_handler.fear_earned == 2
        ), f"Unexpected fear count {self.island.terror_handler.fear_earned}, expected 2"
        self.assert_invaders({
            "cities": 0,
            "towns": 0,
            "explorers": 1,
        })

    def test_crops_wither_and_fade_town_and_city(self):
        self.island.add_piece("town", self.land)
        self.island.add_piece("city", self.land)
        self.input_handler.add_expected_request(
            self.land.cities[0],
            reason="Select town or city to downgrade"
        )

        crops_wither_and_fade.execute({}, self.island)

        assert (
            self.island.terror_handler.fear_earned == 2
        ), f"Unexpected fear count {self.island.terror_handler.fear_earned}, expected 2"
        self.assert_invaders({
            "cities": 0,
            "towns": 2,
            "explorers": 0,
        })

    def test_crops_wither_and_fade_city(self):
        self.island.add_piece("city", self.land)
        self.input_handler.add_expected_request(
            self.land.cities[0],
            reason="Select town or city to downgrade"
        )

        crops_wither_and_fade.execute({}, self.island)

        assert (
            self.island.terror_handler.fear_earned == 2
        ), f"Unexpected fear count {self.island.terror_handler.fear_earned}, expected 2"
        self.assert_invaders({
            "cities": 0,
            "towns": 1,
            "explorers": 0,
        })

    def test_crops_wither_and_fade_empty_land(self):
        crops_wither_and_fade.execute({}, self.island)
        assert (
            self.island.terror_handler.fear_earned == 2
        ), f"Unexpected fear count {self.island.terror_handler.fear_earned}, expected 2"
        self.assert_invaders({
            "cities": 0,
            "towns": 0,
            "explorers": 0,
        })

    def assert_invaders(self, invader_counts):
        assert (
            len(self.land.cities) == invader_counts["cities"]
        ), f"Unexpected cities count: {len(self.land.towns)}, expected {invader_counts['cities']}"
        assert (
            len(self.land.towns) == invader_counts["towns"]
        ), f"Unexpected towns count: {len(self.land.towns)}, expected {invader_counts['towns']}"
        assert (
            len(self.land.explorers) == invader_counts["explorers"]
        ), f"Unexpected explorers count: {len(self.land.explorers)}, expected {invader_counts['explorers']}"


class TestConcealingShadows(unittest.TestCase):

    def setUp(self):
        test_controls = {
            "board": "single_empty_land.json",
        }
        self.input_handler = TestInputHandler()
        self.island = Island(test_controls, self.input_handler)
        self.land = self.island.lands[0]

        self.input_handler.add_expected_request(
            self.land,
            reason="Select target land for concealing shadows"
        )
        test_controls = {
            "board": "single_land_board.json",
            "auto_allocate_damage": True,
            "suppress_end_of_game": True,
        }
        self.ravage_action = RavageAction(test_controls, self.island, self.land, TestInputHandler())

    def test_no_dahan(self):
        self.island.add_piece("town", self.land)
        concealing_shadows.execute({}, self.island)
        self.ravage_action.execute_action()

        assert (
            len(self.land.towns) == 1
        ), f"Unexpected towns count: {len(self.land.towns)}, expected 1"
        assert (
            len(self.land.blight) == 1
        ), f"Unexpected blight count: {len(self.land.blight)}, expected 1"

    def test_with_dahan(self):
        self.island.add_piece("town", self.land)
        self.island.add_piece("dahan", self.land)
        concealing_shadows.execute({}, self.island)
        self.ravage_action.execute_action()
        assert (
            len(self.land.towns) == 0
        ), f"Unexpected towns count: {len(self.land.towns)}, expected 0"
        assert (
            len(self.land.dahan) == 1
        ), f"Unexpected dahan count: {len(self.land.dahan)}, expected 1"
        assert (
            len(self.land.blight) == 1
        ), f"Unexpected blight count: {len(self.land.blight)}, expected 1"
