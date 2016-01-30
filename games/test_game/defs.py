import engine
from engine.signals import sighandler
from engine import bind

@engine.meta.apply
class BourgChar(engine.character.Character):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n = 0

    @sighandler
    def actioned(self, game, player, map, pos):
        x, y, z = pos
        dx, dy = player.x - x, player.y - y
        self.turn(dx, dy)
        player.dialog = self.dialog = engine.dialog.spawn('Hello', 'World', '!', bind.cb(self.set, dialog=None))

    def step(self, game):
        self.n = (self.n + 1) % 5
        if self.n:
            return
        if not self.walk():
            dx, dy = self.direction
            self.turn(-dy, dx)

class BourgChar2(BourgChar):
    @sighandler
    def actioned(self, game, player, map, pos):
        player.dialog = self.dialog = engine.dialog.spawn(
            (
                ('oui', 'cool'),
                ('non',)
            ),
            bind.cb(self.set, dialog=None)
        )
