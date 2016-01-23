from .character import Trainer
from . import meta

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
