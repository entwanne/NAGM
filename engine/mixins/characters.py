from ..gobject import GObject
from ..signals import sighandler
from .. import dialog
from .. import bind

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
    __attributes__ = ('nb_interactions', 'dialogs')
    def __init__(self, **kwargs):
        kwargs.setdefault('nb_interactions', 0)
        kwargs.setdefault('dialogs', ())
        super().__init__(**kwargs)
        self.__end_speach = dialog.Action(callback=bind.cb(self.decr_interactions))

    @sighandler
    def actioned(self, game, player, map, pos):
        x, y, z = pos
        dx, dy = player.x - x, player.y - y
        self.turn(dx, dy)
        self.say(player, *self.dialogs)

    @property
    def moveable(self):
        return super().moveable and not self.nb_interactions

    def say(self, player, *dialogs):
        self.nb_interactions += 1
        dialog.spawn(player, *dialogs)
        dialog.spawn(player, self.__end_speach)

    def decr_interactions(self):
        self.nb_interactions -= 1
