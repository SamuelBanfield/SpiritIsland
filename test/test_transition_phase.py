import copy
import os
import unittest
from typing import List

from spirit_island import launcher
from spirit_island.framework.input_request import InputHandler
from spirit_island.framework.island import Island
from spirit_island.framework.land import Land
from spirit_island.phases.transition_phases import *


class TestTransitionPhase(unittest.TestCase):
    def setUp(self):

        controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")
        self.runner = launcher.Runner(controls_path, InputHandler())

        self.runner.create_island()
        self.runner.create_phases()

    def test_cards_advance(self):
        invader_deck0 = copy.deepcopy(self.runner.island.invader_deck)

        for round_number in range(len(invader_deck0)):
            print("Checking invader track at round: ", round_number + 1)
            track_a = copy.deepcopy(self.runner.island.invader_track)

            self.runner.explore.begin_phase()
            self.runner.cards_advance.begin_phase()
            track_b = copy.deepcopy(self.runner.island.invader_track)

            if len(track_b["discard"]) > 0:
                assert (
                    track_a["ravage"] == track_b["discard"][-1]
                ), "Ravage card not moved into Discard"
            if track_b["ravage"] is not None:
                assert (
                    track_a["build"] == track_b["ravage"]
                ), "Build card not moved to Ravage"

        deck_check = True
        for i, card in enumerate(self.runner.island.invader_track["discard"]):
            if not card == invader_deck0[i]:
                deck_check = False
        assert deck_check, "Not all cards moved to Discard"

    def test_time_passes_on_pieces(self):
        time_passes_phase = copy.deepcopy(self.runner.time_passes_phase)
        lands: List[Land] = time_passes_phase.island.lands
        lands[2].cities[0].health = 1
        lands[2].dahan[0].damage = 5
        lands[7].dahan[1].health = 4

        time_passes_phase.begin_phase()

        expected_city_health = 3
        expected_dahan_damage = 2
        expected_dahan_health = 2
        actual_city_health = lands[2].cities[0].health
        actual_dahan_damage = lands[2].dahan[0].damage
        actual_dahan_health = lands[7].dahan[1].health

        assert (
            actual_city_health == expected_city_health
        ), f"Expected {expected_city_health} city health, it actually has {actual_city_health}"
        assert (
            actual_dahan_damage == expected_dahan_damage
        ), f"Expected {expected_dahan_damage} city health, it actually has {actual_dahan_damage}"
        assert (
            actual_dahan_health == expected_dahan_health
        ), f"Expected {expected_dahan_health} city health, it actually has {actual_dahan_health}"

    def test_time_passes_on_land(self):
        time_passes_phase = copy.deepcopy(self.runner.time_passes_phase)
        lands: List[Land] = time_passes_phase.island.lands
        lands[1].defend = 7
        lands[1].can_build = False
        lands[3].can_build_city = False
        lands[8].fear_generated_in_land = 1

        time_passes_phase.begin_phase()

        expected_defend = 0
        expected_can_build = True
        expected_can_build_city = True
        expected_fear = 0
        actual_defend = lands[1].defend
        actual_can_build = lands[1].can_build
        actual_can_build_city = lands[3].can_build_city
        actual_fear = lands[8].fear_generated_in_land

        assert (
            actual_defend == expected_defend
        ), f"Expected {expected_defend} city health, it actually has {actual_defend}"
        assert (
            actual_can_build == expected_can_build
        ), f"Expected {expected_can_build} city health, it actually has {actual_can_build}"
        assert (
            actual_can_build_city == expected_can_build_city
        ), f"Expected {expected_can_build_city} city health, it actually has {actual_can_build_city}"
        assert (
            actual_fear == expected_fear
        ), f"Expected {expected_fear} city health, it actually has {actual_fear}"
