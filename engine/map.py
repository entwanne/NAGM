from .gobject import GObject
from . import event
from .player import Player
from . import meta

@meta.apply
class Map(GObject):
    __attributes__ = GObject.__attributes__ + ('width', 'height', 'levels', 'tiles', 'zones')

    def __init__(self, **kwargs):
        #kwargs['width']
        #kwargs['height']
        #kwargs['levels']
        #kwargs['tiles']
        kwargs.setdefault('zones', ())
        #self.width, self.height, self.levels = size
        #self.tiles = tiles # map tiles (grounds)
        #self.zones = zones # map zones (battles are thrown by events)
        super().__init__(**kwargs)
        self.neighboars = {} # neighboar maps (for coalescing)
        self.traversables = {}

    @classmethod
    def from_tiles(cls, tiles, zones=()):
        levels = len(tiles)
        height = len(tiles[0]) if levels else 0
        width = len(tiles[0][0]) if height else 0
        return cls(width=width, height=height, levels=levels, tiles=tiles, zones=zones)

    def has_tile(self, pos):
        x, y, z = pos
        return (0 <= x < self.width and 0 <= y < self.height and 0 <= z < len(self.tiles))

    def get_tile(self, pos):
        if not self.has_tile(pos):
            return
        x, y, z = pos
        return self.tiles[z][y][x]

    def get_events(self, pos):
        for e in event.events:
            if e.map == self and e.position == pos:
                yield e

    def on_case(self, pos):
        tile = self.get_tile(pos)
        if tile:
            yield tile
        yield from self.get_events(pos)

    def walk_position(self, pos, dir):
        x, y, z = pos
        tile = self.get_tile(pos)
        if hasattr(tile, 'directions') and dir in tile.directions:
            dx, dy, dz = tile.directions[dir]
            return (x + dx, y + dy, z + dz)
        dx, dy = dir
        return (x + dx, y + dy, z)

    def can_move(self, pos):
        if not self.has_tile(pos):
            return False
        traversable = self.traversables.get(pos)
        if traversable is None:
            for obj in self.on_case(pos):
                traversable = obj.traversable
            self.traversables[pos] = traversable
        return traversable

    def moved(self, game, char, old_map, old_pos, pos):
        old_map.traversables[old_pos] = None
        self.traversables[pos] = None
        if isinstance(char, Player):
            for event in self.on_case(pos):
                if hasattr(event, 'crossed'):
                    event.crossed(game, char, old_map, old_pos, self, pos)

    def action(self, game, player, pos):
        for event in self.on_case(pos):
            if hasattr(event, 'actioned'):
                event.actioned(game, player, self, pos)
