from .character import Trainer

class Player(Trainer):
    "Playable trainer(s)"
    def __init__(self, *args, **kwargs):
        Trainer.__init__(self, *args, **kwargs)
        self.battle = None
        self.dialog = None

    @property
    def moveable(self):
        return self.battle is None and self.dialog is None

    def move(self, *args, **kwargs):
        if not self.moveable:
            return False
        return Trainer.move(self, *args, **kwargs)

    def turn(self, *args, **kwargs):
        if not self.moveable:
            return False
        return Trainer.turn(self, *args, **kwargs)

    def action(self):
        if self.moveable:
            self.send(self.map.action, (self.x + self.dx, self.y + self.dy, self.z))
        elif self.battle:
            self.battle = None
