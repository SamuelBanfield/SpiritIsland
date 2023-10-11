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

        # Retrieve the piece count on the land
        city_count = land.invader_count["city"]
        town_count = land.invader_count["town"]
        explorer_count = land.invader_count["explorer"]
        dahan_count = land.dahan_count

        # Skip if no invaders present
        invader_total = city_count + town_count + explorer_count
        if not invader_total:
            return

        # Calculate the damage to the land and the dahan health
        damage_total = 3 * city_count + 2 * town_count + explorer_count - land.defend
        dahan_health = 2 * dahan_count

        # Blight the land
        land.blight_count += 1

        # Damage the dahan
        if damage_total >= dahan_health and dahan_count:
            land.dahan_count = 0
            dahan_count = 0
        elif dahan_count:
            dahan_health -= damage_total
            dahan_count = int((dahan_health + dahan_health % 2) / 2)
            land.dahan_count = dahan_count

        # Calculate the damage to the invaders and the invader health
        dahan_damage = 2 * dahan_count
        invader_health = 3 * city_count + 2 * town_count + explorer_count

        # Damage the invaders
        city_destroy = 0
        town_destroy = 0
        explorer_destroy = 0
        if dahan_damage > invader_health:
            city_destroy += city_count
            town_destroy += town_count
            explorer_destroy += explorer_count
        else:  # hard-coded method
            dahan_damage_remaining = dahan_damage

            while dahan_damage_remaining > 0:
                if dahan_damage_remaining >= 3 and city_count > 0:
                    city_destroy += 1
                    dahan_damage_remaining -= 3
                elif dahan_damage_remaining >= 2 and town_count > 0:
                    town_destroy += 1
                    dahan_damage_remaining -= 2
                elif explorer_count > 0:
                    explorer_destroy += 1
                    dahan_damage_remaining -= 1
                else:
                    break

        land.invader_count["city"] -= city_destroy
        land.invader_count["town"] -= town_destroy
        land.invader_count["explorer"] -= explorer_destroy

        self.island.generate_fear(2 * city_destroy + town_destroy)

        self.check_end_game()
        print("Ravage Action Done")


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

        # Retrieve the piece count on the land
        city_count = land.invader_count["city"]
        town_count = land.invader_count["town"]
        explorer_count = land.invader_count["explorer"]

        # Skip if no invaders present
        invader_total = city_count + town_count + explorer_count
        if not invader_total:
            return

        if town_count > city_count:
            land.invader_count["city"] += 1
        else:
            land.invader_count["town"] += 1

        print("Build Action Done")


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

        if (land.invader_count["city"] + land.invader_count["town"]) > 0:
            source = True
        elif land.number in [1, 2, 3]:
            source = True
        else:
            for adj_land_no in lands_adj:
                adj_land = lands_list[adj_land_no]
                if (adj_land.invader_count["city"] + adj_land.invader_count["town"]) > 0:
                    source = True
                    break

        if source:
            land.invader_count["explorer"] += 1

        print("Explore Action Done")
