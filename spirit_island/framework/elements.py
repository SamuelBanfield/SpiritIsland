from typing import Dict


class Element:
    """A spirit island element"""

    def __init__(self, name):
        self._name = name
    
    def __eq__(self, other):
        return self._name == other._name
    
    def __hash__(self):
        return hash(self._name)

    def __str__(self):
        return f"{self._name} element"

# The spirit island elements
sun = Element("Sun")
moon = Element("Moon")
fire = Element("Fire")
air = Element("Air")
water = Element("Water")
earth = Element("Earth")
plant = Element("Plant")
animal = Element("Animal")

class ElementalThreshold:
    """Represents an elemental requirement"""

    def __init__(self, elements: Dict[Element, int]):
        """
        :param elemnts: a dictionary containing the elements that make up
        this threshold
        """
        self._elements = elements

    def __eq__(self, other):
        return self._elements == other._elements

    def is_satisfied_by(self, available_elements):
        """
        :param available_elements: the elements available for this play of the card

        Return whether there are sufficient elements available to reach this threshold.
        """
        for element, number in self._elements.items():
            if element not in available_elements or number > available_elements[element]:
                return False
        return True

    def __hash__(self) -> int:
        """Hash, thresholds may be useful as keys for innates with many thresholds"""
        return sum(number * hash(element) for element, number in self._elements.items())

    def __str__(self):
        return f"Elemental threshold: {','.join((str(number) + element._name for element, number in self._elements.items()))}"

no_elemental_requirement = ElementalThreshold([])