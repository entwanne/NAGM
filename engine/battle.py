from .gobject import GObject
from .beast import Beast

class Battle(GObject):
    "Battle between two trainers (or beasts)"
    def __init__(self, *trainers):
        self.trainers, self.beasts = [], []
        for trainer in trainers:
            if isinstance(trainer, Beast):
                self.trainers.append(None)
                self.beasts.append(trainer)
            else:
                self.trainers.append(trainer)
                self.beasts.append(getattr(trainer, 'beast', None))
                trainer.battle = self

    def action(self, game, player):
        if any(beast.ko for beast in self.beasts if beast):
            for trainer in self.trainers:
                if trainer:
                    trainer.battle = None
        self.beasts[0].attack(self.beasts[1])
