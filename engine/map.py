from .gobject import GObject
from . import event
from .player import Player
from . import meta
from .signals import sighandler

@meta.apply
class BaseMap(GObject):
    "A map is an object where events can be placed"

    def get_events(self, pos):
        'List all game events at a specific position on the map'
        for e in event.events:
            if e.map == self and e.position == pos:
                yield e

    def walk_position(self, pos, dir):
        'Get the next case given a position and a direction'
        x, y, z = pos
        dx, dy = dir
        return (x + dx, y + dy, z)

    def can_move(self, pos):
        'Returns True if a position is free'
        return True

    @sighandler
    def moved(self, game, char, old_map, old_pos, pos):
        'Handler called when an event has moved on a map'
        if isinstance(char, Player):
            for event in self.get_events(pos):
                # Call events on the map that are crossed
                if hasattr(event, 'crossed'):
                    event.crossed(game, char, old_map, old_pos, self, pos)

    @sighandler
    def action(self, game, player, pos):
        'Handler called when a player press action-button'
        for event in self.get_events(pos):
            if hasattr(event, 'actioned'):
                event.actioned(game, player, self, pos)

@meta.apply
class Map(BaseMap):
    "Tiled map"
    __attributes__ = ('width', 'height', 'levels', 'tiles', 'zones')

    def __init__(self, **kwargs):
        kwargs.setdefault('zones', ())
        #self.width, self.height, self.levels = size
        #self.tiles = tiles # map tiles (grounds)
        #self.zones = zones # map zones (battles are thrown by events)
        super().__init__(**kwargs)
        self.neighboars = {} # neighboar maps (for coalescing)
        self.traversables = {}

    @classmethod
    def from_tiles(cls, tiles, zones=()):
        '''Construct a map from tiles, computing map size
        `tiles` is a list of levels, which are list of lines, which are list of tiles
        '''
        levels = len(tiles)
        height = len(tiles[0]) if levels else 0
        width = len(tiles[0][0]) if height else 0
        return cls(width=width, height=height, levels=levels, tiles=tiles, zones=zones)

    def has_tile(self, pos):
        'Returns True if a position belongs to a tile on the map'
        x, y, z = pos
        return (0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.levels)

    def get_tile(self, pos):
        'Get the tile of a given position'
        if not self.has_tile(pos):
            return
        x, y, z = pos
        return self.tiles[z][y][x]

    def get_events(self, pos):
        'Get the events and the tile of a given position'
        tile = self.get_tile(pos)
        if tile:
            yield tile
        yield from super().get_events(pos)

    def walk_position(self, pos, dir):
        x, y, z = pos
        tile = self.get_tile(pos)
        # Handle relief
        if hasattr(tile, 'directions') and dir in tile.directions:
            dx, dy, dz = tile.directions[dir]
            return (x + dx, y + dy, z + dz)
        dx, dy = dir
        return (x + dx, y + dy, z)

    def can_move(self, pos):
        if not self.has_tile(pos):
            return False
        # Handle traversable tiles/events
        traversable = self.traversables.get(pos)
        if traversable is None:
            for obj in self.get_events(pos):
                traversable = obj.traversable
            self.traversables[pos] = traversable
        return traversable

    @sighandler
    def moved(self, game, char, old_map, old_pos, pos):
        old_map.traversables[old_pos] = None
        self.traversables[pos] = None
        super().moved(game, char, old_map, old_pos, pos)
