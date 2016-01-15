from .gobject import GObject
from .signals import signals

class Event(GObject):
    "All objects that can interact with player (on the map)"
    def __init__(self, pos=(0, 0, 0), map=None):
        self.x, self.y, self.z = pos
        self.map = map

    def send(self, *args):
        signals.append(args)
