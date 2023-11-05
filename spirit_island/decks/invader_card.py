from .card_base import Card


class InvaderCard(Card):
    """Cards used for the invader deck."""

    def __init__(self, terrain_types: list, invader_stage: int):
        super().__init__()

        self.terrains = terrain_types
        self.stage = invader_stage

    def __eq__(self, other):
        """See if a card is equivalent for testing"""
        return self.terrains == other.terrains and self.stage == other.stage

    def __hash__(self):
        """Hash so that this can be used in dictionaries"""
        terrain_hash = hash(tuple(self.terrains))
        stage_hash = hash(self.stage)
        return terrain_hash ^ stage_hash
