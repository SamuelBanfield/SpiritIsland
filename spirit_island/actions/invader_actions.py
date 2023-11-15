import json
import os

from spirit_island.actions.action_base import Action
from spirit_island.framework.input_request import InputHandler, InputRequest
from spirit_island.framework.island import Island
from spirit_island.framework.land import Land
from spirit_island.framework.logger import logger


class InvaderAction(Action):

    def __init__(self, controls: dict, island: Island, land: Land, input_handler: InputHandler):
        super().__init__(controls, island)
        self.land = land
        self._input_handler = input_handler

class RavageAction(InvaderAction):
    """Ravage action in a single land."""

    def __init__(self, controls: dict, island: Island, land: Land, input_handler: InputHandler):
        """
        Initialise.
        :param controls: path to debug_controls file
        :param island: Island object
        :param land: the target land of this action
        """
        super().__init__(controls, island, land, input_handler)

    def execute_action(self):
        """Performs the ravage action in the land number specified."""

        # Skip if no invaders present
        invader_all = self.land.cities + self.land.towns + self.land.explorers
        if not len(invader_all):
            return

        # Calculate the damage to the land and the dahan health
        damage_total = sum(invader.damage for invader in invader_all)

        # Blight the land
        if damage_total >= 2:
            self.island.add_piece("blight", self.land)
            if self.land.get_blight_count() > 1:
                land_options = [land for land in self.island.lands if self.island.are_lands_adjacent(land, self.land)]
                land = self._input_handler.request_land_input(
                    "Select land for blight cascade",
                    land_options
                )
                logger.info(f"Cascading blight into land '{land.id}'")
                self.island.add_piece("blight", land)

        # Damage the dahan
        if len(self.land.dahan) + damage_total:
            if damage_total >= sum(dahan.health for dahan in self.land.dahan):
                self.land.dahan.clear()
            else:
                remaining_damage = damage_total
                # Damage dahan in the most lethal way by ordering them by health
                dahan_health_dict = {dahan.id: dahan for dahan in self.land.dahan}
                sorted_dict = dict(
                    sorted(dahan_health_dict.items(), key=lambda item: item[1].health)
                )
                for dahan in sorted_dict.values():
                    if remaining_damage >= dahan.health:
                        remaining_damage -= dahan.health
                        dahan.health = 0
                    else:
                        dahan.health -= remaining_damage
                        remaining_damage = 0
                # Replace dahan list with a new list of surviving dahan
                surviving_dahan = [dahan for dahan in self.land.dahan if dahan.health > 0]
                self.land.dahan = surviving_dahan

        # Calculate the damage to the invaders from dahan counterattack
        dahan_damage = sum(dahan.damage for dahan in self.land.dahan)

        # Damage the invaders
        if self._controls["auto_allocate_damage"]:
            if dahan_damage > 3 * len(self.land.cities) + 2 * len(self.land.towns) + len(
                self.land.explorers
            ):
                for city in self.land.cities:
                    self.island.terror_handler.add_fear(city.base_fear)
                self.land.cities.clear()
                for town in self.land.towns:
                    self.island.terror_handler.add_fear(town.base_fear)
                self.land.towns.clear()
                for explorer in self.land.explorers:
                    self.island.terror_handler.add_fear(explorer.base_fear)
                self.land.explorers.clear()
            else:  # hard-coded method
                dahan_damage_remaining = dahan_damage

                while dahan_damage_remaining > 0:
                    if dahan_damage_remaining >= 3 and len(self.land.cities):
                        self.island.terror_handler.add_fear(self.land.cities[0].base_fear)
                        self.land.cities.pop(0)
                        dahan_damage_remaining -= 3
                    elif dahan_damage_remaining >= 2 and len(self.land.towns):
                        self.island.terror_handler.add_fear(self.land.towns[0].base_fear)
                        self.land.towns.pop(0)
                        dahan_damage_remaining -= 2
                    elif len(self.land.explorers):
                        self.island.terror_handler.add_fear(self.land.explorers[0].base_fear)
                        self.land.explorers.pop(0)
                        dahan_damage_remaining -= 1
                    else:
                        print("dahan counterattack damage miscalculation!")
                        break
        else:
            # Choose dahan damage in the UI
            pass

        print(f"Ravage - Action Done in land {self.land.id}")
        self.check_end_game()


class BuildAction(InvaderAction):
    """Build action in a single land."""

    def __init__(self, controls: dict, island: Island, land: Land, input_handler: InputHandler):
        """
        Initialise.
        :param controls: path to debug_controls file
        :param island: Island object
        :param land: the target land of this action
        """
        super().__init__(controls, island, land, input_handler)

    def execute_action(self):
        """Performs the build action in the land number specified."""

        # Skip if the land is forbidden from building this turn
        if not self.land.can_build:
            print(f"Skipped build in {self.land.id}")
            return

        # Skip if no invaders present
        invader_all = self.land.cities + self.land.towns + self.land.explorers
        if not len(invader_all):
            return

        if len(self.land.towns) > len(self.land.cities) and self.land.can_build_city:
            self.island.add_piece("city", self.land)
        elif len(self.land.towns) <= len(self.land.cities):
            self.island.add_piece("town", self.land)

        print(f"Build - Action Done in land {self.land.id}")
        self.check_end_game()


class ExploreAction(InvaderAction):
    """Explore action in a single land."""

    def __init__(self, controls: dict, island: Island, land: Land, input_handler: InputHandler):
        """
        Initialise.
        :param controls: path to debug_controls file
        :param island: Island object
        :param land: the target land of this action
        """
        super().__init__(controls, island, land, input_handler)

    def execute_action(self):
        """Performs the explore action in the land number specified."""
        lands_list = self.island.lands
        rel_path = os.path.relpath(__file__ + "/../../resources/board_adjacencies.json")
        with open(rel_path) as adj_file:
            adj_dict = json.load(adj_file)
            lands_adj = adj_dict[str(self.land.number)]

        # Check if it has source of exploration
        source = False

        if (len(self.land.cities) + len(self.land.towns)) > 0:
            source = True
        elif self.land.number in [1, 2, 3]:
            source = True
        else:
            for adj_land_no in lands_adj:
                adj_land = lands_list[adj_land_no]
                if (len(adj_land.cities) + len(adj_land.towns)) > 0:
                    source = True
                    break

        if source:
            self.island.add_piece("explorer", self.land)

        print(f"Explore - Action Done in land {self.land.id}")
        self.check_end_game()
