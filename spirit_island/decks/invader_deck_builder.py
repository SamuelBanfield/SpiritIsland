import random
from typing import List

from .invader_card import InvaderCard


class InvaderDeckBuilder:
    """Class to build the invader deck."""

    def __init__(self):
        self.stage_1 = ["mountain", "sand", "jungle", "wetland"]
        self.stage_2 = ["mountain", "sand", "jungle", "wetland", "coast"]
        self.stage_3 = [
            ["sand", "mountain"],
            ["mountain", "jungle"],
            ["mountain", "wetland"],
            ["jungle", "sand"],
            ["sand", "wetland"],
            ["jungle", "wetland"],
        ]

    def generate_deck(self) -> List:
        """Function to be called when user wants a newly generated invader deck."""
        invader_deck = (
            self.generate_stage_1() + self.generate_stage_2() + self.generate_stage_3()
        )

        return invader_deck

    def build_deck(self) -> List:
        """Function to be called when user wants the fixed invader deck."""
        invader_deck = (
            self.build_stage_1() + self.build_stage_2() + self.build_stage_3()
        )

        return invader_deck

    def build_stage_1(self) -> List:
        pool = ["sand", "jungle", "mountain"]
        phase_1_deck = []

        for terrain in pool:
            new_card = InvaderCard([terrain], 1)
            phase_1_deck.append(new_card)

        return phase_1_deck

    def build_stage_2(self) -> List:
        pool = ["wetland", "coast", "mountain", "sand"]
        phase_1_deck = []

        for terrain in pool:
            new_card = InvaderCard([terrain], 2)
            phase_1_deck.append(new_card)

        return phase_1_deck

    def build_stage_3(self) -> List:
        pool = [
            ["mountain", "jungle"],
            ["mountain", "wetland"],
            ["jungle", "sand"],
            ["sand", "wetland"],
            ["jungle", "wetland"],
        ]
        phase_1_deck = []

        for terrain in pool:
            new_card = InvaderCard(terrain, 3)
            phase_1_deck.append(new_card)

        return phase_1_deck

    def generate_stage_1(self) -> List:
        pool = random.sample(self.stage_1, 3)
        phase_1_deck = []

        for terrain in pool:
            new_card = InvaderCard([terrain], 1)
            phase_1_deck.append(new_card)

        return phase_1_deck

    def generate_stage_2(self) -> List:
        pool = random.sample(self.stage_2, 4)
        phase_2_deck = []

        for terrain in pool:
            new_card = InvaderCard([terrain], 2)
            phase_2_deck.append(new_card)

        return phase_2_deck

    def generate_stage_3(self) -> List:
        pool = random.sample(self.stage_3, 5)
        phase_3_deck = []

        for terrain in pool:
            new_card = InvaderCard(terrain, 3)
            phase_3_deck.append(new_card)

        return phase_3_deck
