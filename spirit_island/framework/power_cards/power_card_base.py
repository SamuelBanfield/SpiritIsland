from spirit_island.framework.island import Island
from spirit_island.framework.elements import Element
from typing import Dict, Literal


class SpiritPower:

    def __init__(self, name, energy, elements, action: callable, speed: Literal["fast", "slow"]) -> None:
        """
        :param name: string name of this power
        :param cost: the cost to play this power
        :param elements: an array (?) with the containing the elements this card provides
        :param action: a callable that executes the spirit action. It should take as arguments:
            - elements_available: the elements available, may become the spirit once they exist
            - island: the island
        :param speed: whether this power is fast or slow
        """
        self.name = name
        self.energy = energy
        self.elements = elements
        self.action = action
        self.speed = speed

    def execute(self, elements: Dict[Element, int], island: Island) -> None:
        """
        :param elements: the elements available to the spirit for this play of the card
        :param island: the island
        """
        self.action(elements, island)





