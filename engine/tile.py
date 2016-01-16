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

    def cross(self, game, player):
        print('BATTLE')
        player.walk(1,0)

class Teleport(EventTile):
    "Teleport player"
    traversable = True
    def __init__(self, pos, map_name=None):
        self.pos = pos
        self.map_name = map_name

    def cross(self, game, player):
        if player.walking:
            map = game.maps[self.map_name] if self.map_name else None
            player.move(*self.pos, map=map)
