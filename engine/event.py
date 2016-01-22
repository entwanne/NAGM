from .gobject import GObject

class Event(GObject):
    "All objects that can interact with player (on the map)"

    __attributes__ = GObject.__attributes__ + ('position', 'map')

    traversable = True
    def __init__(self, **kwargs):
        kwargs.setdefault('position', (0, 0, 0))
        kwargs.setdefault('map', None)
        GObject.__init__(self, **kwargs)

    @property
    def position(self):
        return (self.x, self.y, self.z)

    @position.setter
    def position(self, pos):
        self.x, self.y, self.z = pos

events = []
