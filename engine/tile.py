from .gobject import GObject
from .battle import Battle
from . import dialog
from . import meta
from .signals import sighandler

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

    __attributes__ = ('zone',)

    traversable = True
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zone.area += 1

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

# deprecated
@meta.apply
class Hole(Tile):
    "Hole"
    traversable = True
    @sighandler
    def crossed(self, game, player, old_map, old_pos, map, pos):
        x, y, z = pos
        player.move(x, y, z - 1)

@meta.apply
class Edge(Tile):
    "Edge"
    traversable = True
    directions = {(0, -1): (0, -1, -1)}

@meta.apply
class Water(Tile):
    pass
