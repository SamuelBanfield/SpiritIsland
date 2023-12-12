import copy
import os
import unittest

from spirit_island import launcher
from spirit_island.test_support.input_handler import TestInputHandler
from spirit_island.actions.invader_actions import RavageAction
from spirit_island.framework.island import Island
from spirit_island.test_support import phase_util


class TestInvaderPhase(unittest.TestCase):
    def setUp(self):

        controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")
        self.runner = launcher.Runner(controls_path, TestInputHandler())

        self.runner.create_island()
        self.runner.create_phases()

    def test_explore(self):
        lands0 = copy.deepcopy(self.runner.island.lands)

        phase_util.run_phase(self.runner.explore)

        explore_card = self.runner.island.invader_track["explore"]
        terrains = explore_card.terrains
        print("Exploring Terrains: ", terrains)

        lands1 = self.runner.island.lands

        for land0 in lands0:
            for land1 in lands1:
                if land0 == land1:
                    print("Check carried out in land: ", land0.id)
                    print(
                        "Explorers before: ",
                        land0.get_explorer_count(),
                        " | Explorers after: ",
                        land1.get_explorer_count(),
                    )
                    if (
                        land0.terrain in terrains
                    ):  # Need to add check for invader source
                        assert (
                            land0.get_explorer_count() + 1 == land1.get_explorer_count()
                        ), "Explorer not added in exploring terrain"
                    else:
                        assert (
                            land0.get_explorer_count() == land1.get_explorer_count()
                        ), "Explorer added in non-exploring terrain"

    def test_build(self):
        phase_util.run_phase(self.runner.explore)
        phase_util.run_phase(self.runner.cards_advance)

        lands0 = copy.deepcopy(self.runner.island.lands)

        phase_util.run_phase(self.runner.build)

        build_card = self.runner.island.invader_track["build"]
        terrains = build_card.terrains
        print("Building Terrains: ", terrains)

        lands1 = self.runner.island.lands

        for land0 in lands0:
            for land1 in lands1:
                if land0 == land1:
                    print("Check carried out in land: ", land0.id)
                    print(
                        "Explorers/Towns/Cities before: ",
                        land0.get_explorer_count(),
                        land0.get_town_count(),
                        land0.get_city_count(),
                        " | Explorers/Towns/Cities after: ",
                        land1.get_explorer_count(),
                        land1.get_town_count(),
                        land1.get_city_count(),
                    )
                    if land0.terrain in terrains:
                        if land0.get_town_count() > land0.get_city_count():
                            assert (
                                land0.get_city_count() + 1 == land1.get_city_count()
                            ), "City not built in building terrain"
                        else:
                            assert (
                                land0.get_town_count() + 1 == land1.get_town_count()
                            ), "Town not built in building terrain"
                    else:
                        assert (
                            land0.get_explorer_count() == land1.get_explorer_count()
                            and land0.get_town_count() == land1.get_town_count()
                            and land0.get_city_count() == land1.get_city_count()
                        ), "Built in non-building terrain"

    def test_ravage(self):  # Ravage will not cascade blight yet
        phase_util.run_phase(self.runner.explore)
        phase_util.run_phase(self.runner.cards_advance)

        phase_util.run_phase(self.runner.build)
        phase_util.run_phase(self.runner.explore)
        phase_util.run_phase(self.runner.cards_advance)

        lands0 = copy.deepcopy(self.runner.island.lands)

        phase_util.run_phase(self.runner.ravage)

        ravage_card = self.runner.island.invader_track["ravage"]
        terrains = ravage_card.terrains
        print("Ravaging Terrains: ", terrains)

        lands1 = self.runner.island.lands

        for land0 in lands0:
            for land1 in lands1:
                if land0 == land1:
                    print("Check carried out in land: ", land0.number)
                    print(
                        "Explorers/Towns/Cities/Dahan before: ",
                        land0.get_explorer_count(),
                        land0.get_town_count(),
                        land0.get_city_count(),
                        land0.get_dahan_count(),
                        " | Explorers/Towns/Cities/Dahan after: ",
                        land1.get_explorer_count(),
                        land1.get_town_count(),
                        land1.get_city_count(),
                        land1.get_dahan_count(),
                    )
                    if land0.terrain in terrains:
                        invader_damage = (
                            land0.get_explorer_count()
                            + 2 * land0.get_town_count()
                            + 3 * land0.get_city_count()
                        )
                        dahan_health = 2 * land0.get_dahan_count()
                        if invader_damage >= 2:
                            assert (
                                land0.get_blight_count() + 1 == land1.get_blight_count()
                            ), "Blight not added to blighted land"
                        assert (
                            dahan_health - invader_damage <= 2 * land1.get_dahan_count()
                        ), "Not enough dahan killed during ravage"
                        invader_health = invader_damage
                        dahan_damage = 2 * land1.get_dahan_count()
                        assert (
                            invader_health - dahan_damage
                            <= land1.get_explorer_count()
                            + 2 * land1.get_town_count()
                            + 3 * land1.get_city_count()
                        ), "Dahan counterattack damage miscalculation"
                    else:
                        assert (
                            land0.get_explorer_count() == land1.get_explorer_count()
                            and land0.get_town_count() == land1.get_town_count()
                            and land0.get_city_count() == land1.get_city_count()
                            and land0.get_dahan_count() == land1.get_dahan_count()
                            and land0.get_blight_count() == land1.get_blight_count()
                        ), "Ravaged in non-ravaging terrain"


class TestInvaderActions(unittest.TestCase):
    def test_ravage_clear_dahan(self):
        test_controls = {
            "board": "single_land_board.json",
            "auto_allocate_damage": True,
        }
        island = Island(test_controls, TestInputHandler())
        land = island.lands[0]
        ravage = RavageAction(test_controls, island, land, TestInputHandler())
        land.dahan.pop(0)

        ravage.execute_action()

        assert len(land.dahan) == 0, f"Unexpected number of dahan: {len(land.dahan)}"
        assert len(land.cities) == 1, f"Unexpected number of cities: {len(land.cities)}"
        assert len(land.towns) == 1, f"Unexpected number of towns: {len(land.towns)}"
        assert (
            len(land.explorers) == 2
        ), f"Unexpected number of explorers: {len(land.explorers)}"

    def test_ravage_dahan_survive(self):
        test_controls = {
            "board": "single_land_board.json",
            "auto_allocate_damage": True,
        }
        island = Island(test_controls, TestInputHandler())
        land = island.lands[0]
        ravage = RavageAction(test_controls, island, land, TestInputHandler())

        ravage.execute_action()

        assert len(land.dahan) == 1, f"Unexpected number of dahan: {len(land.dahan)}"
        assert len(land.cities) == 1, f"Unexpected number of cities: {len(land.cities)}"
        assert len(land.towns) == 0, f"Unexpected number of towns: {len(land.towns)}"
        assert (
            len(land.explorers) == 2
        ), f"Unexpected number of explorers: {len(land.explorers)}"
        assert (
            land.dahan[0].health == 1
        ), f"Unexpected health of the surviving dahan: {land.dahan[0].health}"

    def test_ravage_lethality(self):
        test_controls = {
            "board": "single_land_board.json",
            "auto_allocate_damage": True,
        }
        island = Island(test_controls, TestInputHandler())
        land = island.lands[0]
        ravage = RavageAction(test_controls, island, land, TestInputHandler())
        land.dahan[3].health = 1
        land.towns.pop(0)
        # Invaders do 5 damage but should still kill 3 dahan
        # The 1 surviving dahan should kill the 2 explorers

        ravage.execute_action()

        assert len(land.dahan) == 1, f"Unexpected number of dahan: {len(land.dahan)}"
        assert len(land.cities) == 1, f"Unexpected number of cities: {len(land.cities)}"
        assert len(land.towns) == 0, f"Unexpected number of towns: {len(land.towns)}"
        assert (
            len(land.explorers) == 0
        ), f"Unexpected number of explorers: {len(land.explorers)}"
        assert (
            land.dahan[0].health == 2
        ), f"Unexpected health of surviving dahan: {land.dahan[0].health}"

class TestDefence(unittest.TestCase):

    def test_defend_with_dahan(self):
        test_controls = {
            "board": "single_land_board.json",
            "auto_allocate_damage": True,
            "suppress_end_of_game": True,
        }
        island = Island(test_controls, TestInputHandler())
        land = island.lands[0]
        land.defend = 6
        ravage = RavageAction(test_controls, island, land, TestInputHandler())
        ravage.execute_action()

        assert len(land.dahan) == 4, f"Unexpected number of dahan: {len(land.dahan)}"
        assert len(land.cities) == 0, f"Unexpected number of cities: {len(land.cities)}"
        assert len(land.towns) == 0, f"Unexpected number of towns: {len(land.towns)}"
        assert (
            len(land.explorers) == 0
        ), f"Unexpected number of explorers: {len(land.explorers)}"
        

