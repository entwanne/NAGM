from .gobject import GObject
from .beast import Beast

class Battle(GObject):
    "Battle between two trainers (or beasts)"
    def __init__(self, trainer1, trainer2):
        if isinstance(trainer1, Beast):
            self.beast1, self.trainer1 = trainer1, None
        else:
            self.beast1, self.trainer1 = None, trainer1
            trainer1.battle = self
        if isinstance(trainer2, Beast):
            self.beast2, self.trainer2 = trainer2, None
        else:
            self.beast2, self.trainer2 = None, trainer2
            trainer2.battle = self

    def action(self, game, player):
        if self.trainer1 is not None:
            self.trainer1.battle = None
        if self.trainer2 is not None:
            self.trainer2.battle = None
