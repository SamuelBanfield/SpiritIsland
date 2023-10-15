import copy
import os
import unittest

from spirit_island import launcher


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
                    print("Check carried out in land: ", land0.number)
                    print(
                        "Explorers before: ",
                        land0.invader_count["explorer"],
                        " | Explorers after: ",
                        land1.invader_count["explorer"],
                    )
                    if (
                        land0.terrain in terrains
                    ):  # Need to add check for invader source
                        assert (
                            land0.invader_count["explorer"] + 1
                            == land1.invader_count["explorer"]
                        ), "Explorer not added in exploring terrain"
                    else:
                        assert (
                            land0.invader_count["explorer"]
                            == land1.invader_count["explorer"]
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
                    print("Check carried out in land: ", land0.number)
                    print(
                        "Explorers/Towns/Cities before: ",
                        land0.invader_count["explorer"],
                        land0.invader_count["town"],
                        land0.invader_count["city"],
                        " | Explorers/Towns/Cities after: ",
                        land1.invader_count["explorer"],
                        land1.invader_count["town"],
                        land1.invader_count["city"],
                    )
                    if land0.terrain in terrains:
                        if land0.invader_count["town"] > land0.invader_count["city"]:
                            assert (
                                land0.invader_count["city"] + 1
                                == land1.invader_count["city"]
                            ), "City not built in building terrain"
                        else:
                            assert (
                                land0.invader_count["town"] + 1
                                == land1.invader_count["town"]
                            ), "Town not built in building terrain"
                    else:
                        assert (
                            land0.invader_count["explorer"]
                            == land1.invader_count["explorer"]
                            and land0.invader_count["town"]
                            == land1.invader_count["town"]
                            and land0.invader_count["city"]
                            == land1.invader_count["city"]
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
                        land0.invader_count["explorer"],
                        land0.invader_count["town"],
                        land0.invader_count["city"],
                        land0.dahan_count,
                        " | Explorers/Towns/Cities/Dahan after: ",
                        land1.invader_count["explorer"],
                        land1.invader_count["town"],
                        land1.invader_count["city"],
                        land1.dahan_count,
                    )
                    if land0.terrain in terrains:
                        invader_damage = (
                            land0.invader_count["explorer"]
                            + 2 * land0.invader_count["town"]
                            + 3 * land0.invader_count["city"]
                        )
                        dahan_health = 2 * land0.dahan_count
                        if invader_damage >= 2:
                            assert (
                                land0.blight_count + 1 == land1.blight_count
                            ), "Blight not added to blighted land"
                        assert (
                            dahan_health - invader_damage <= 2 * land1.dahan_count
                        ), "Not enough dahan killed during ravage"
                        invader_health = invader_damage
                        dahan_damage = 2 * land1.dahan_count
                        assert (
                            invader_health - dahan_damage
                            <= land1.invader_count["explorer"]
                            + 2 * land1.invader_count["town"]
                            + 3 * land1.invader_count["city"]
                        ), "Dahan counterattack damage miscalculation"
                    else:
                        assert (
                            land0.invader_count["explorer"]
                            == land1.invader_count["explorer"]
                            and land0.invader_count["town"]
                            == land1.invader_count["town"]
                            and land0.invader_count["city"]
                            == land1.invader_count["city"]
                            and land0.dahan_count == land1.dahan_count
                            and land0.blight_count == land1.blight_count
                        ), "Ravaged in non-ravaging terrain"
