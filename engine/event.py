from .gobject import GObject

class Event(GObject):
    "All objects that can interact with player (on the map)"
    def __init__(self):
        self.x, self.y, self.z = 0, 0, 0
        self.map = None
