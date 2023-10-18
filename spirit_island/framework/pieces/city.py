from .invader_piece import InvaderPiece


class City(InvaderPiece):
    """Store the status of an invader piece"""

    def __init__(self):
        super().__init__()

        self.base_health = 3
        self.base_damage = 3
        self.base_fear = 2

        self.reset_damage()
        self.reset_health()
