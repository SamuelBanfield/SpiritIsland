from spirit_island.decks.card_base import Card
from spirit_island.framework.island import Island


class FearCardBase(Card):
    """Cards used for the fear deck."""

    def __init__(self):
        super().__init__()
        self.name = ""
        self.level1_text = ""
        self.level2_text = ""
        self.level3_text = ""

    def __eq__(self, other):
        """See if a card is equivalent for testing."""
        return self.name == other.name

    def level1_effect(self, island):
        """Placeholder for terror level 1 effect."""
        pass

    def level2_effect(self, island):
        """Placeholder for terror level 2 effect."""
        pass

    def level3_effect(self, island):
        """Placeholder for terror level 3 effect."""
        pass


class FearCardTest(FearCardBase):
    def __init__(self):
        super().__init__()


class OverseasTrade(FearCardBase):
    def __init__(self):
        super().__init__()
        self.name = "Overseas Trade Seems Safer"
        self.id = 0
        self.level1_text = "Defend 3 in all Coastal lands."
        self.level2_text = "Defend 6 in all Coastal lands. Skip all Build Actions in Coastal lands that would Add a City."
        self.level3_text = (
            "Defend 9 in all Coastal lands. Skip all Build Actions in Coastal lands."
        )

    def level1_effect(self, island):
        """Overseas Trade terror level 1"""
        print(f"Terror level 1 effect: {self.level1_text}")
        for land in island.lands:
            if land.is_coastal:
                land.defend += 3

    def level2_effect(self, island):
        """Overseas Trade terror level 2"""
        for land in island.lands:
            if land.is_coastal:
                land.defend += 6
                land.can_build_city = False

    def level3_effect(self, island):
        """Overseas Trade terror level 3"""
        for land in island.lands:
            if land.is_coastal:
                land.defend += 9
                land.can_build = False
