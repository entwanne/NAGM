from .gobject import GObject

class Event(GObject):
    "All objects that can interact with player (on the map)"
    traversable = True
    def __init__(self, pos=(0, 0, 0), map=None):
        self.position = pos
        self.map = map

    @property
    def position(self):
        return (self.x, self.y, self.z)

    @position.setter
    def position(self, pos):
        self.x, self.y, self.z = pos

events = []
