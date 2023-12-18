import unittest
from spirit_island.actions.invader_actions import RavageAction

from spirit_island.framework.power_cards.shadows_flicker_like_flame import mantle_of_dread, favors_called_due, concealing_shadows, crops_wither_and_fade
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

class TestFavorsCalledDue(unittest.TestCase):

    def setUp(self):
        test_controls = {
            "board": "board_d.json",
        }
        self.input_handler = TestInputHandler()
        self.island = Island(test_controls, self.input_handler)

    def test_favors_called_due(self):
        land_one = self.island.lands[1]
        land_seven = self.island.lands[7]
        target_land = self.island.lands[8]
        self.island.add_piece("explorer", target_land)
        self.input_handler.add_expected_request(
            target_land,
            reason="Select target land for favors called due"
        )
        for dahan in land_one.dahan + land_seven.dahan:
            self.input_handler.add_expected_request(
                selection=dahan,
                reason="Select dahan to gather"
            )
        favors_called_due.execute({}, self.island)
        
        assert (
            len(target_land.dahan) == 4
        ), f"Unexpected dahan count: {len(target_land.dahan)}, expected 4"
        assert (
            len(land_one.dahan) == 0
        ), f"Unexpected dahan count: {len(land_one.dahan)}, expected 0"
        assert (
            len(land_seven.dahan) == 0
        ), f"Unexpected dahan count: {len(land_seven.dahan)}, expected 0"
        assert (
            self.island.terror_handler.fear_earned == 3
        ), f"Unexpected fear count {self.island.terror_handler.fear_earned}, expected 3"

    def test_favors_called_due_no_adjacent_dahan(self):
        land_one = self.island.lands[1]
        land_one.dahan.clear()
        land_seven = self.island.lands[7]
        land_seven.dahan.clear()
        # There are now no gatherable dahan in any adjacent lands
        target_land = self.island.lands[8]
        self.input_handler.add_expected_request(
            target_land,
            reason="Select target land for favors called due"
        )
        favors_called_due.execute({}, self.island)
        
        assert (
            len(target_land.dahan) == 0
        ), f"Unexpected dahan count: {len(target_land.dahan)}, expected 0"
        assert (
            self.island.terror_handler.fear_earned == 0
        ), f"Unexpected fear count {self.island.terror_handler.fear_earned}, expected 0"

class TestMantleOfDread(unittest.TestCase):

    def setUp(self):
        test_controls = {
            "board": "empty_board.json",
            "auto_allocate_damage": True,
            "suppress_end_of_game": True,
        }
        self.input_handler = TestInputHandler()
        self.island = Island(test_controls, self.input_handler)

    def assert_towns_and_explorers(self, land, towns, explorers):
        assert (
            len(land.towns) == towns
        ), f"Unexpected towns count: {len(land.towns)}, expected {towns}"
        assert (
            len(land.explorers) == explorers
        ), f"Unexpected explorers count: {len(land.explorers)}, expected {explorers}"

    def test_mantle_of_dread_empty_land(self):
        target_land = self.island.lands[8]
        self.input_handler.add_expected_request(
            target_land,
            reason="Select target land for mantle of dread"
        )

        mantle_of_dread.execute({}, self.island)
    
        assert (
            self.island.terror_handler.fear_earned == 2
        ), f"Unexpected fear count {self.island.terror_handler.fear_earned}, expected 2"
        self.assert_towns_and_explorers(target_land, 0, 0)

    def test_single_explorer_and_town(self):
        land_one = self.island.lands[1]
        land_seven = self.island.lands[7]
        target_land = self.island.lands[8]
        self.island.add_piece("town", target_land)
        self.island.add_piece("explorer", target_land)
        self.input_handler.add_expected_request(
            target_land,
            reason="Select target land for mantle of dread"
        )
        self.input_handler.add_expected_request(
            land_one,
            reason="Select land to push explorer to"
        )
        self.input_handler.add_expected_request(
            land_seven,
            reason="Select land to push town to"
        )

        mantle_of_dread.execute({}, self.island)

        assert (
            self.island.terror_handler.fear_earned == 2
        ), f"Unexpected fear count {self.island.terror_handler.fear_earned}, expected 2"
        self.assert_towns_and_explorers(target_land, 0, 0)
        self.assert_towns_and_explorers(land_one, 0, 1)
        self.assert_towns_and_explorers(land_seven, 1, 0)

    def test_multiple_explorers_and_towns(self):
        land_one = self.island.lands[1]
        land_seven = self.island.lands[7]
        target_land = self.island.lands[8]
        self.island.add_piece("town", target_land)
        self.island.add_piece("town", target_land)
        self.island.add_piece("explorer", target_land)
        self.island.add_piece("explorer", target_land)
        self.input_handler.add_expected_request(
            target_land,
            reason="Select target land for mantle of dread"
        )
        self.input_handler.add_expected_request(
            target_land.explorers[0],
            reason="Select explorer to push"
        )
        self.input_handler.add_expected_request(
            land_one,
            reason="Select land to push explorer to"
        )
        self.input_handler.add_expected_request(
            target_land.towns[0],
            reason="Select town to push"
        )
        self.input_handler.add_expected_request(
            land_seven,
            reason="Select land to push town to"
        )

        mantle_of_dread.execute({}, self.island)

        assert (
            self.island.terror_handler.fear_earned == 2
        ), f"Unexpected fear count {self.island.terror_handler.fear_earned}, expected 2"

        self.assert_towns_and_explorers(target_land, 1, 1)
        self.assert_towns_and_explorers(land_one, 0, 1)
        self.assert_towns_and_explorers(land_seven, 1, 0)
