import json
import os

from spirit_island.actions.action_base import Action
from spirit_island.framework.island import Island
from spirit_island.framework.land import Land


class RavageAction(Action):
    """Ravage action in a single land."""

    def __init__(self, controls: dict, island: Island):
        """
        Initialise.
        :param controls: path to debug_controls file
        :param island: Island object
        """
        super().__init__(controls, island)

    def execute_action(self, land: Land):
        """Performs the ravage action in the land number specified."""

        # Skip if no invaders present
        invader_all = land.cities + land.towns + land.explorers
        if not len(invader_all):
            return

        # Calculate the damage to the land and the dahan health
        damage_total = 0
        for invader in invader_all:
            damage_total += invader.damage

        # Blight the land
        if damage_total >= 2:
            self.island.add_piece("blight", land)

        # Damage the dahan
        if damage_total >= 2 * len(land.dahan) and len(land.dahan):
            land.dahan.clear()
        elif not damage_total:
            pass
        elif len(land.dahan):
            remaining_damage = (
                damage_total  # Clears dahan from top to bottom, not most lethal
            )
            while remaining_damage > 0:
                for dahan in land.dahan:
                    for h in range(dahan.health):
                        dahan.health -= 1
                        remaining_damage -= 1
                    land.dahan.pop(0)

        # Calculate the damage to the invaders and the invader health
        dahan_damage = 0
        for dahan in land.dahan:
            dahan_damage += dahan.damage

        # Damage the invaders
        if dahan_damage > 3 * len(land.cities) + 2 * len(land.towns) + len(
            land.explorers
        ):
            for city in land.cities:
                self.island.add_fear(city.base_fear)
            land.cities.clear()
            for town in land.towns:
                self.island.add_fear(town.base_fear)
            land.towns.clear()
            for explorer in land.explorers:
                self.island.add_fear(explorer.base_fear)
            land.explorers.clear()
        else:  # hard-coded method
            dahan_damage_remaining = dahan_damage

            while dahan_damage_remaining > 0:
                if dahan_damage_remaining >= 3 and len(land.cities):
                    self.island.add_fear(land.cities[0].base_fear)
                    land.cities.pop(0)
                    dahan_damage_remaining -= 3
                elif dahan_damage_remaining >= 2 and len(land.towns):
                    self.island.add_fear(land.towns[0].base_fear)
                    land.towns.pop(0)
                    dahan_damage_remaining -= 2
                elif len(land.explorers):
                    self.island.add_fear(land.explorers[0].base_fear)
                    land.explorers.pop(0)
                    dahan_damage_remaining -= 1
                else:
                    print("dahan counterattack damage miscalculation!")
                    break

        print(f"Ravage - Action Done in land {land.id}")
        self.check_end_game()


class BuildAction(Action):
    """Build action in a single land."""

    def __init__(self, controls: dict, island: Island):
        """
        Initialise.
        :param controls: path to debug_controls file
        :param island: Island object
        """
        super().__init__(controls, island)

    def execute_action(self, land: Land):
        """Performs the build action in the land number specified."""

        # Skip if no invaders present
        invader_all = land.cities + land.towns + land.explorers
        if not len(invader_all):
            return

        if len(land.towns) > len(land.cities):
            self.island.add_piece("city", land)
        else:
            self.island.add_piece("town", land)

        print(f"Build - Action Done in land {land.id}")
        self.check_end_game()


class ExploreAction(Action):
    """Explore action in a single land."""

    def __init__(self, controls: dict, island: Island):
        """
        Initialise.
        :param controls: path to debug_controls file
        :param island: Island object
        """
        super().__init__(controls, island)

    def execute_action(self, land: Land):
        """Performs the explore action in the land number specified."""
        lands_list = self.island.lands
        rel_path = os.path.relpath(__file__ + "/../../resources/board_adjacencies.json")
        with open(rel_path) as adj_file:
            adj_dict = json.load(adj_file)
            lands_adj = adj_dict[str(land.number)]

        # Check if it has source of exploration
        source = False

        if (len(land.cities) + len(land.towns)) > 0:
            source = True
        elif land.number in [1, 2, 3]:
            source = True
        else:
            for adj_land_no in lands_adj:
                adj_land = lands_list[adj_land_no]
                if (len(adj_land.cities) + len(adj_land.towns)) > 0:
                    source = True
                    break

        if source:
            self.island.add_piece("explorer", land)

        print(f"Explore - Action Done in land {land.id}")
        self.check_end_game()
