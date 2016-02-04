import engine
from engine.signals import sighandler
from engine import bind

@engine.meta.apply
class BourgChar(engine.character.Character):
    __attributes__ = ('moving',)

    def __init__(self, **kwargs):
        kwargs.setdefault('moving', True)
        super().__init__(**kwargs)
        self.n = 0

    @sighandler
    def actioned(self, game, player, map, pos):
        x, y, z = pos
        dx, dy = player.x - x, player.y - y
        self.turn(dx, dy)
        self.moving = False
        engine.dialog.spawn(player, 'Hello', 'World', '!', signal=bind.cb(self.set, moving=True))

    def step(self, game):
        self.n = (self.n + 1) % 5
        if self.n:
            return
        if not self.walk():
            dx, dy = self.direction
            self.turn(-dy, dx)

    @property
    def moveable(self):
        return super().moveable and self.moving

class BourgChar2(BourgChar):
    @sighandler
    def actioned(self, game, player, map, pos):
        self.moving = False
        sig = bind.cb(self.set, moving=True)
        engine.dialog.spawn_choice(
            player,
            ('oui', bind.cb(engine.dialog.spawn, bind._, 'cool', signal=sig)),
            ('non', sig))
