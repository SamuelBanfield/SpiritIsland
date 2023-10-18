from .piece import Piece


class InvaderPiece(Piece):
    """Store the status of an invader piece"""

    def __init__(self):
        super().__init__()

        self.base_health = 0
        self.base_damage = 0
        self.base_fear = 0

        self.health = 0
        self.damage = 0

        self.is_strifed = False

    def reset_health(self):
        """Reset the health of the piece back to its default"""
        self.health = self.base_health

    def reset_damage(self):
        """Reset the damage of the piece back to its default"""
        self.damage = self.base_damage

