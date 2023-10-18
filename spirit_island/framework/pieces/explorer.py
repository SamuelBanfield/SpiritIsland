from .invader_piece import InvaderPiece


class Explorer(InvaderPiece):
    """Store the status of an invader piece"""

    def __init__(self):
        super().__init__()

        self.base_health = 1
        self.base_damage = 1
        self.base_fear = 0

        self.reset_damage()
        self.reset_health()
