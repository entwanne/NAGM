from .character import Trainer
from . import meta
from .dialog import Choice
from .bind import callback

@meta.apply
class Player(Trainer):
    "Playable trainer(s)"
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
        self.dialog = Choice(choices=choices, signals=signals)
