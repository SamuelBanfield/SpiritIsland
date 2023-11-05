class TerrorHandler:
    """The Island creates a terror handler to hold all fear related properties."""

    def __init__(self, handler_args: dict):
        # Terror level stuff
        self.terror_level = 1
        # Fear card stuff
        self.fear_card_discard_pile = []
        self.fear_cards_pending = 0
        self.fear_cards_to_next_level = 3
        # Fear pool stuff
        self.fear_earned = 0
        self.fear_capacity = handler_args.get("n_players", 1) * 4

    def add_fear(self, fear_added):
        """Add fear to fear pool and earn the necessary fear cards."""
        self.fear_earned += fear_added
        while self.fear_earned >= self.fear_capacity:
            self.earn_fear_card()
            self.fear_earned -= self.fear_capacity

    def earn_fear_card(self):
        """Add one to pending fear cards. Then check terror level."""
        self.fear_cards_pending += 1
        self.fear_cards_to_next_level -= 1

        self.update_terror_level()

    def update_terror_level(self):
        """Updates the terror level after a fear card had been earned"""
        if self.fear_cards_to_next_level == 0:
            self.terror_level += 1
            self.fear_cards_to_next_level = 3
