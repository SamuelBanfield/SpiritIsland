import copy
import os
import unittest

from spirit_island import launcher
from spirit_island.decks.fear_cards import *
from spirit_island.phases.fear_card_phase import FearPhase
from spirit_island.test_support import phase_util

class TestFearCardOverseasTrade(unittest.TestCase):
    def setUp(self):

        controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")
        self.runner = launcher.Runner(controls_path)

        self.runner.create_island()
        self.runner.create_phases()

        self.test_card = OverseasTrade()

    def test_fear_card_overseas_trade_1(self):
        fear_phase: FearPhase = self.runner.fear_card_phase
        fear_phase.island.terror_handler.terror_level = 1

        fear_phase.perform_fear_card(self.test_card, fear_phase.island)

        expected_defends = {
            "0": 0,
            "1": 3,
            "2": 3,
            "3": 3,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
        }
        actual_defends = {land.number: land.defend for land in fear_phase.island.lands}

        assert (
            expected_defends == actual_defends
        ), f"Defend values {actual_defends} do not match expected values {expected_defends}"

    def test_fear_card_overseas_trade_2(self):
        fear_phase: FearPhase = self.runner.fear_card_phase
        fear_phase.island.terror_handler.terror_level = 2

        fear_phase.perform_fear_card(self.test_card, fear_phase.island)

        expected_defends = {
            "0": 0,
            "1": 6,
            "2": 6,
            "3": 6,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
        }
        actual_defends = {land.number: land.defend for land in fear_phase.island.lands}

        phase_util.run_phase(self.runner.explore)
        phase_util.run_phase(self.runner.cards_advance)
        fear_phase.island.lands[2].terrain = "sand"
        for i in range(3):
            phase_util.run_phase(self.runner.build)

        expected_invaders_land2 = {"Cities": 1, "Towns": 2}
        actual_invaders_land2 = {
            "Cities": len(fear_phase.island.lands[2].cities),
            "Towns": len(fear_phase.island.lands[2].towns),
        }

        assert (
            expected_defends == actual_defends
        ), f"Defend values {actual_defends} do not match expected values {expected_defends}"

        assert (
            expected_invaders_land2 == actual_invaders_land2
        ), f"Invaders {actual_invaders_land2} do not match expected invaders {expected_invaders_land2}"

    def test_fear_card_overseas_trade_3(self):
        fear_phase: FearPhase = self.runner.fear_card_phase
        fear_phase.island.terror_handler.terror_level = 3

        fear_phase.perform_fear_card(self.test_card, fear_phase.island)

        expected_defends = {
            "0": 0,
            "1": 9,
            "2": 9,
            "3": 9,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
        }
        actual_defends = {land.number: land.defend for land in fear_phase.island.lands}

        phase_util.run_phase(self.runner.explore)
        phase_util.run_phase(self.runner.cards_advance)
        fear_phase.island.lands[2].terrain = "sand"
        for i in range(3):
            phase_util.run_phase(self.runner.build)

        expected_invaders_land2 = {"Cities": 1, "Towns": 0}
        actual_invaders_land2 = {
            "Cities": len(fear_phase.island.lands[2].cities),
            "Towns": len(fear_phase.island.lands[2].towns),
        }

        assert (
            expected_defends == actual_defends
        ), f"Defend values {actual_defends} do not match expected values {expected_defends}"

        assert (
            expected_invaders_land2 == actual_invaders_land2
        ), f"Invaders {actual_invaders_land2} do not match expected invaders {expected_invaders_land2}"
