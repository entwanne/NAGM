from .gobject import GObject
from .battle import Battle

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

    def crossed(self, game, player, old_map, old_pos, map, pos):
        beast = self.zone.random_beast()
        player.battle = Battle(player, beast)
        print('A wild', beast.name, 'appears')

class Teleport(Tile):
    "Teleport player"
    traversable = True
    def __init__(self, pos, map_name=None):
        self.pos = pos
        self.map_name = map_name

    def crossed(self, game, player, old_map, old_pos, map, pos):
        if old_map and isinstance(old_map.get_tile(old_pos), Teleport):
            return
        map = game.maps[self.map_name] if self.map_name else None
        player.move(*self.pos, map=map)

class Tree(Tile):
    "Tree"

class Rock(Tile):
    "Rock"

class Stairs(Tile):
    "Stairs"
    traversable = True
    def __init__(self, directions):
        self.directions = directions

class Hole(Tile):
    "Hole"
    traversable = True
    def crossed(self, game, player, old_map, old_pos, map, pos):
        x, y, z = pos
        player.move(x, y, z - 1)
