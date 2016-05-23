from .gobject import GObject
from .battle import Battle
from . import dialog
from . import meta
from .signals import sighandler

from enum import Enum

class Ground(Enum):
    GROUND = 0
    WATER = 1

class TileMeta(meta.GObjectMeta):
    'Metaclass for all tiles (for type-checking)'

    def __instancecheck__(self, tile):
        if super().__instancecheck__(tile):
            return True
        if hasattr(tile, '__isinstance__'):
            return tile.__isinstance__(self)
        return False

@meta.apply
class Tile(GObject, metaclass=TileMeta):
    """All tiles ("voxels") on a map
    have some properties: traversable, etc.
    """
    traversable = False
    ground = Ground.GROUND

@meta.apply
class Grass(Tile):
    "Normal grass"
    traversable = True

@meta.apply
class HighGrass(Tile):
    "High grass (battles)"

    __attributes__ = ('zone',)
    traversable = True

    @classmethod
    def spawn(cls, **kwargs):
        tile = cls(**kwargs)
        tile.zone.area += 1
        return tile

    @sighandler
    def crossed(self, game, player, old_map, old_pos, map, pos):
        beast = self.zone.maybe_beast()
        if beast is not None:
            Battle.from_args(player, beast)
            dialog.spawn(player, 'A wild {} appears'.format(beast.name))

@meta.apply
class Teleport(Tile):
    "Teleport player"

    __attributes__ = ('pos', 'map_name')

    traversable = True
    def __init__(self, **kwargs):
        kwargs.setdefault('map_name', None)
        super().__init__(**kwargs)

    @sighandler
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

    __attributes__ = ('directions',)
    traversable = True

@meta.apply
class Hole(Tile):
    "Hole"

    traversable = True

    @sighandler
    def crossed(self, game, player, old_map, old_pos, map, pos):
        self.send(player.fall)

# deprecated
@meta.apply
class Edge(Tile):
    "Edge"
    traversable = True
    directions = {(0, -1): (0, -1, -1)}

@meta.apply
class Water(Tile):
    "Water"
    traversable = False
    ground = Ground.WATER
    dialogs = ("Wanna surfin?", ('oui', None, 'non', None))

    @sighandler
    def actioned(self, game, player, map, pos):
        dialog.spawn(player, *self.dialogs)

@meta.apply
class Over(Tile):
    __attributes__ = ('tiles',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.traversable = self.tiles[-1].traversable

    def __isinstance__(self, cls):
        return any(isinstance(tile, cls) for tile in self.tiles)

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError as e:
            for tile in self.tiles:
                if hasattr(tile, name):
                    return getattr(tile, name)
            raise e

class over:
    def __init__(self, *tiles_cls):
        self.tiles_cls = tiles_cls

    def __call__(self, **kwargs):
        tiles = tuple(cls() for cls in self.tiles_cls)
        return Over(tiles=tiles, **kwargs)
