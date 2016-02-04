from .character import Trainer
from . import meta
from .dialog import Choice
from .bind import callback

@meta.apply
class Player(Trainer):
    "Playable trainer(s)"

    #__attributes__ = ('dialogs',)
    __attributes__ = ('dialog',)

    def __init__(self, **kwargs):
        #kwargs.setdefault('dialogs', [])
        kwargs.setdefault('dialog', None)
        super().__init__(**kwargs)

    def action(self):
        if self.dialog:
            self.send(self.dialog.action)
        elif self.battle:
            self.send(self.battle.action)
        else:
            self.send(self.map.action, self.map.walk_position(self.position, self.direction))

    def battle_step(self, battle, beast):
        attacks = ((att.name, callback(battle.attack, beast, att))
                   for att in beast.attacks)
        choices, signals = zip(*attacks)
        attacks = Choice(choices=choices, signals=signals)
        self.dialog = Choice(
            choices=('Attack', 'Fuite'),
            signals=(callback(self.set, dialog=attacks), callback(battle.end)))

    @property
    def moveable(self):
        return super().moveable and self.dialog is None
