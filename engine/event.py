from .gobject import GObject
from . import meta

@meta.apply
class Event(GObject):
    '''All objects that can interact with player (on the map)
    Events have a method `step` that is called at each iteration of the game loop
    '''

    __attributes__ = ('position', 'map')

    traversable = False

    def __init__(self, **kwargs):
        kwargs.setdefault('position', (0, 0, 0))
        kwargs.setdefault('map', None)
        super().__init__(**kwargs)

    @classmethod
    def spawn(cls, **kwargs):
        'Spawn an event on the game'
        event = cls(**kwargs)
        events.append(event)
        return event

    # + method to set map at None ?

    def remove(self):
        'Remove an event from the map/game'
        self.map = None
        events.remove(self)

    @property
    def position(self):
        return (self.x, self.y, self.z)

    @position.setter
    def position(self, pos):
        self.x, self.y, self.z = pos

@meta.apply
class Timer(Event):
    'Send a signal when a clock is finished'

    __attributes__ = ('clock', 'signal')

    def step(self, game):
        if not self.clock.finished:
            return
        game.events.remove(self)
        self.send(self.signal)

events = []
