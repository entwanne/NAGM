from .gobject import GObject
from . import meta

@meta.apply
class Event(GObject):
    "All objects that can interact with player (on the map)"

    __attributes__ = ('position', 'map')

    traversable = True
    def __init__(self, **kwargs):
        kwargs.setdefault('position', (0, 0, 0))
        kwargs.setdefault('map', None)
        super().__init__(**kwargs)

    @property
    def position(self):
        return (self.x, self.y, self.z)

    @position.setter
    def position(self, pos):
        self.x, self.y, self.z = pos

@meta.apply
class Timer(Event):
    __attributes__ = ('clock', 'signal')

    def step(self, game):
        if not self.clock.finished:
            return
        game.events.remove(self)
        self.send(self.signal)

events = []
