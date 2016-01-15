from .gobject import GObject
from .event import Event

class Tile(GObject):
    """All tiles ("voxels") on a map
    have some properties: traversable, etc.
    """
    traversable = False

class EventTile(Event, Tile):
    "Tiles that interact with player (stairs)"

class Grass(Tile):
    "Normal grass"
    traversable = True

class HighGrass(EventTile):
    "High grass (battles)"
    traversable = True
    def __init__(self, zone):
        self.zone = zone
