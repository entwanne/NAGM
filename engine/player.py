from .character import Trainer

class Player(Trainer):
    "Playable trainer(s)"
    def action(self):
        self.send(self.map.action, (self.x + self.dx, self.y + self.dy, self.z))
