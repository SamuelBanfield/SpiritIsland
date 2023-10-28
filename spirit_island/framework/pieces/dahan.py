from .piece import Piece


class Dahan(Piece):
    """Store the status of an invader piece"""

    def __init__(self):
        super().__init__()
        self.type = "dahan"

        self.base_health = 2
        self.base_damage = 2

        self.health = 0
        self.damage = 0

        self.reset_damage()
        self.reset_health()

    def reset_health(self):
        """Reset the health of the piece back to its default"""
        self.health = self.base_health

    def reset_damage(self):
        """Reset the damage of the piece back to its default"""
        self.damage = self.base_damage
