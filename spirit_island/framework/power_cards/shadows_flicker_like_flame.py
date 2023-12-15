import math
from typing import Dict

from spirit_island.framework.power_cards.power_card_base import SpiritPower
from spirit_island.framework.elements import Element, no_elemental_requirement, sun, moon, fire, air, water, earth, plant, animal
from spirit_island.framework.island import Island
from spirit_island.framework.land import Land


def _concealing_shadows(available_elements: Dict[Element, int], island: Island):
    target_land = island._input_handler.request_land_input(
        "Select target land for concealing shadows",
        island.lands,
    )
    target_land.dahan_defend = math.inf

def _crops_wither_and_fade(available_elements: Dict[Element, int], island: Island):
    target_land = island._input_handler.request_land_input(
        "Select target land for crops wither and fade",
        island.lands,
    )
    buildings = target_land.towns + target_land.cities
    if len(buildings) >= 1:
        building_to_downgrade = island._input_handler.request_land_content_input(
            "Select town or city to downgrade",
            buildings,
        )
        if building_to_downgrade in target_land.cities:
            target_land.cities.remove(building_to_downgrade)
            island.add_piece("town", target_land)
        elif building_to_downgrade in target_land.towns:
            target_land.towns.remove(building_to_downgrade)
            island.add_piece("explorer", target_land)
        else:
            raise ValueError(f"Building {building_to_downgrade} was not found in land {target_land}")

    island.terror_handler.add_fear(2)

def _favors_called_due(available_elements: Dict[Element, int], island: Island):
    target_land = island._input_handler.request_land_input(
        "Select target land for favors called due",
        island.lands,
    )
    def get_gatherable_dahan():
        gatherable_dahan = []
        for land in island.lands:
            if island.are_lands_adjacent(target_land, land):
                gatherable_dahan += land.dahan
        return gatherable_dahan
    for _ in range(4):
        options = get_gatherable_dahan()
        print(options)
        if not options:
            break
        dahan_to_gather = island._input_handler.request_land_content_input(
            "Select dahan to gather",
            options,
        )
        island.gather_to_land(dahan_to_gather, target_land)
    invaders = target_land.explorers + target_land.towns + target_land.cities
    if target_land.dahan and invaders and len(target_land.dahan) > len(invaders):
        island.terror_handler.add_fear(3)

def _mantle_of_dread(available_elements: Dict[Element, int], island: Island):
    island.terror_handler.add_fear(2)
    target_land = island._input_handler.request_land_input(
        "Select target land for mantle of dread",
        island.lands,
    )
    if explorers := target_land.explorers:
        if len(explorers) > 1:
            explorer = island._input_handler.request_land_content_input(
                "Select explorer to push",
                explorers
            )
        else:
            explorer = explorers[0]
        land_pushed_to = island._input_handler.request_land_input(
            "Select land to push explorer to",
            island.get_lands_adjacent_to_land(target_land),
        )
        island.gather_to_land(explorer, land_pushed_to)
    if towns := target_land.towns:
        if len(towns) > 1:
            town = island._input_handler.request_land_content_input(
                "Select town to push",
                towns
            )
        else:
            town = towns[0]
        land_pushed_to = island._input_handler.request_land_input(
            "Select land to push town to",
            island.get_lands_adjacent_to_land(target_land),
        )
        island.gather_to_land(town, land_pushed_to)


concealing_shadows = SpiritPower(
    name="concealing_shadows",
    energy=0,
    elements=[moon, air],
    action=_concealing_shadows,
    speed="fast"
)

crops_wither_and_fade = SpiritPower(
    name="crops_wither_and_fade",
    energy=1,
    elements=[moon, fire, plant],
    action=_crops_wither_and_fade,
    speed="slow"
)

favors_called_due = SpiritPower(
    name="favors_called_due",
    energy=1,
    elements=[moon, air, animal],
    action=_favors_called_due,
    speed="slow"
)

mantle_of_dread = SpiritPower(
    name="mantle_of_dread",
    energy=1,
    elements=[moon, fire, air],
    action=_mantle_of_dread,
    speed="slow"
)

POWERS = [concealing_shadows, crops_wither_and_fade, favors_called_due, mantle_of_dread]