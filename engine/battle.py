from .gobject import GObject
from .beast import Beast
from . import meta
from .signals import sighandler

@meta.apply
class Battle(GObject):
    "Battle between two trainers (or beasts)"

    __attributes__ = ('trainers', 'beasts')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for trainer in self.trainers:
            if trainer:
                trainer.battle = self

    @classmethod
    def from_args(cls, *args):
        args = (
            (None, obj) if isinstance(obj, Beast)
            else (obj, getattr(obj, 'beast', None))
            for obj in args
        )
        trainers, beasts = zip(*args)
        return cls(trainers=trainers, beasts=beasts)

    @sighandler
    def action(self, game, player):
        if any(beast.ko for beast in self.beasts if beast):
            for trainer in self.trainers:
                if trainer:
                    trainer.battle = None
        self.beasts[0].attack(self.beasts[1])
