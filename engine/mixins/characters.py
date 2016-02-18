from ..gobject import GObject
from ..signals import sighandler
from .. import dialog

class InfiniteWalker:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__n = 0
        self.__speed = 5

    def step(self, game):
        self.__n = (self.__n + 1) % self.__speed
        if self.__n:
            return
        if not self.walk():
            dx, dy = self.direction
            self.turn(-dy, dx)

class Speaker(GObject):
    __attributes__ = ('moving',)
    def __init__(self, **kwargs):
        kwargs.setdefault('moving', True)
        super().__init__(**kwargs)

    @sighandler
    def actioned(self, game, player, map, pos):
        x, y, z = pos
        dx, dy = player.x - x, player.y - y
        self.turn(dx, dy)
        self.moving = False
        dialog.spawn(player, *self.dialogs)

    @property
    def moveable(self):
        return super().moveable and self.moving
