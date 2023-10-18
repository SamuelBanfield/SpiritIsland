from .invader_piece import InvaderPiece


class Town(InvaderPiece):
    """Store the status of an invader piece"""

    def __init__(self):
        super().__init__()

        self.base_health = 2
        self.base_damage = 2
        self.base_fear = 1

        self.reset_damage()
        self.reset_health()
