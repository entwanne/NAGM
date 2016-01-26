from .gobject import GObject
from .battle import Battle
from .dialog import Message
from . import meta

@meta.apply
class Tile(GObject):
    """All tiles ("voxels") on a map
    have some properties: traversable, etc.
    """
    traversable = False

@meta.apply
class Grass(Tile):
    "Normal grass"
    traversable = True

@meta.apply
class HighGrass(Tile):
    "High grass (battles)"

    __attributes__ = Tile.__attributes__ + ('zone',)

    traversable = True
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zone.area += 1

    def crossed(self, game, player, old_map, old_pos, map, pos):
        beast = self.zone.maybe_beast()
        if beast is not None:
            Battle.from_args(player, beast)
            Message(msg='A wild {} appears'.format(beast.name), dest=player)

@meta.apply
class Teleport(Tile):
    "Teleport player"

    __attributes__ = Tile.__attributes__ + ('pos', 'map_name')

    traversable = True
    def __init__(self, **kwargs):
        kwargs.setdefault('map_name', None)
        super().__init__(**kwargs)

    def crossed(self, game, player, old_map, old_pos, map, pos):
        if old_map and isinstance(old_map.get_tile(old_pos), Teleport):
            return
        map = game.maps[self.map_name] if self.map_name else None
        player.move(*self.pos, map=map)

@meta.apply
class Tree(Tile):
    "Tree"

@meta.apply
class Rock(Tile):
    "Rock"

@meta.apply
class Stairs(Tile):
    "Stairs"

    __attributes__ = Tile.__attributes__ + ('directions',)
    traversable = True

@meta.apply
class Hole(Tile):
    "Hole"
    traversable = True
    def crossed(self, game, player, old_map, old_pos, map, pos):
        x, y, z = pos
        player.move(x, y, z - 1)
