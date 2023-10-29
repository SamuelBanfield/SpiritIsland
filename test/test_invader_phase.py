import copy
import os
import unittest

from spirit_island import launcher
from spirit_island.actions.invader_actions import RavageAction
from spirit_island.framework.island import Island


class TestInvaderPhase(unittest.TestCase):
    def setUp(self):

        controls_path = os.path.relpath(__file__ + "/../../debug_controls.json")
        self.runner = launcher.Runner(controls_path)

        self.runner.create_island()
        self.runner.create_phases()

    def test_explore(self):
        lands0 = copy.deepcopy(self.runner.island.lands)

        self.runner.explore.execute_phase()

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

    def test_cards_advance(self):
        invader_deck0 = copy.deepcopy(self.runner.island.invader_deck)

        for round_number in range(len(invader_deck0)):
            print("Checking invader track at round: ", round_number + 1)
            track_a = copy.deepcopy(self.runner.island.invader_track)

            self.runner.explore.execute_phase()
            self.runner.cards_advance.execute_phase()
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

    def test_build(self):
        self.runner.explore.execute_phase()
        self.runner.cards_advance.execute_phase()

        lands0 = copy.deepcopy(self.runner.island.lands)

        self.runner.build.execute_phase()

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
        self.runner.explore.execute_phase()
        self.runner.cards_advance.execute_phase()

        self.runner.build.execute_phase()
        self.runner.explore.execute_phase()
        self.runner.cards_advance.execute_phase()

        lands0 = copy.deepcopy(self.runner.island.lands)

        self.runner.ravage.execute_phase()

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
        island = Island(test_controls)
        ravage = RavageAction(test_controls, island)
        land = island.lands[0]
        land.dahan.pop(0)

        ravage.execute_action(land)

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
        island = Island(test_controls)
        ravage = RavageAction(test_controls, island)
        land = island.lands[0]

        ravage.execute_action(land)

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
        island = Island(test_controls)
        ravage = RavageAction(test_controls, island)
        land = island.lands[0]
        land.dahan[3].health = 1
        land.towns.pop(0)
        # Invaders do 5 damage but should still kill 3 dahan
        # The 1 surviving dahan should kill the 2 explorers

        ravage.execute_action(land)

        assert len(land.dahan) == 1, f"Unexpected number of dahan: {len(land.dahan)}"
        assert len(land.cities) == 1, f"Unexpected number of cities: {len(land.cities)}"
        assert len(land.towns) == 0, f"Unexpected number of towns: {len(land.towns)}"
        assert (
            len(land.explorers) == 0
        ), f"Unexpected number of explorers: {len(land.explorers)}"
        assert (
            land.dahan[0].health == 2
        ), f"Unexpected health of surviving dahan: {land.dahan[0].health}"
