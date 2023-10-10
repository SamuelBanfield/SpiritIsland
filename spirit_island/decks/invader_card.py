from .card import Card


class InvaderCard(Card):
    """Cards used for the invader deck."""

    def __init__(self, terrain_types: list, invader_phase: int):
        super().__init__()

        self.terrains = terrain_types
        self.phase = invader_phase
