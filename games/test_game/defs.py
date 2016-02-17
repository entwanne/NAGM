import engine
from engine.signals import sighandler
from engine import bind

@engine.meta.apply
class BourgChar(engine.character.Character):
    __attributes__ = ('moving',)

    def __init__(self, **kwargs):
        kwargs.setdefault('moving', True)
        super().__init__(**kwargs)
        self.__n = 0
        self.__messages = [
            engine.dialog.Message(msg='Hello'),
            engine.dialog.Message(msg='World'),
            engine.dialog.Message(msg='!', signal=bind.cb(self.set, moving=True)),
        ]

    @sighandler
    def actioned(self, game, player, map, pos):
        x, y, z = pos
        dx, dy = player.x - x, player.y - y
        self.turn(dx, dy)
        self.moving = False
        engine.dialog.spawn(player, *self.__messages)

    def step(self, game):
        self.__n = (self.__n + 1) % 5
        if self.__n:
            return
        if not self.walk():
            dx, dy = self.direction
            self.turn(-dy, dx)

    @property
    def moveable(self):
        return super().moveable and self.moving

class BourgChar2(BourgChar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sig = bind.cb(self.set, moving=True)
        self.__message = engine.dialog.Message(msg='cool', signal=sig)
        self.__choice = engine.dialog.Choice(
            choices=('oui', 'non'),
            signals=(bind.cb(engine.dialog.spawn, bind._, self.__message), sig),
        )

    @sighandler
    def actioned(self, game, player, map, pos):
        self.moving = False
        player.add_dialog(self.__choice)
