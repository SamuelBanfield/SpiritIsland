from typing import Dict

from spirit_island.framework.power_cards.power_card_base import SpiritPower
from spirit_island.framework.elements import Element, no_elemental_requirement, sun, moon, fire, air, water, earth, plant, animal
from spirit_island.framework.island import Island
from spirit_island.framework.land import Land


def _concealing_shadows(available_elements: Dict[Element, int], island: Island):
    pass

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
    pass

def _mantle_of_dread(available_elements: Dict[Element, int], island: Island):
    pass

# concealing_shadows = SpiritPower(
#     name="concealing_shadows",
#     energy=0,
#     elements=[moon, air],
#     action=_concealing_shadows,
#     speed="fast"
# )

crops_wither_and_fade = SpiritPower(
    name="crops_wither_and_fade",
    energy=0,
    elements=[moon, air],
    action=_crops_wither_and_fade,
    speed="fast"
)

# favors_called_due = SpiritPower(
#     name,
#     energy,
#     [],
#     actions,
#     target_provider,
#     speed
# )

# mantle_of_dread = SpiritPower(
#     name,
#     energy,
#     [],
#     actions,
#     target_provider,
#     speed
# )