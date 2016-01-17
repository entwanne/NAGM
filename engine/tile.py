from .gobject import GObject

class Tile(GObject):
    """All tiles ("voxels") on a map
    have some properties: traversable, etc.
    """
    traversable = False

class Grass(Tile):
    "Normal grass"
    traversable = True

class HighGrass(Tile):
    "High grass (battles)"
    traversable = True
    def __init__(self, zone):
        self.zone = zone

    def cross(self, game, player):
        print('BATTLE', self.zone.random_family().name)
        player.turn(1,0)
        player.walk()

class Teleport(Tile):
    "Teleport player"
    traversable = True
    def __init__(self, pos, map_name=None):
        self.pos = pos
        self.map_name = map_name

    def cross(self, game, player):
        if player.walking:
            map = game.maps[self.map_name] if self.map_name else None
            player.move(*self.pos, map=map)

class Tree(Tile):
    "Tree"
