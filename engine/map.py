from .gobject import GObject
from .event import Event

class Map(GObject):
    def __init__(self, size, tiles, events=(), zones=()):
        self.width, self.height, self.levels = size
        self.tiles = tiles # map tiles (grounds)
        self.events = events # map events (objects, characters, event tiles, etc.)
        self.zones = zones # map zones (battles are thrown by events)
        self.neighboars = {} # neighboar maps (for coalescing)
        self.traversables = {}

    @classmethod
    def from_tiles(cls, tiles, events=(), zones=()):
        levels = len(tiles)
        height = len(tiles[0]) if levels else 0
        width = len(tiles[0][0]) if height else 0
        return cls((width, height, levels), tiles, events, zones)

    def can_move(self, pos):
        if not self.has_tile(pos):
            return False
        traversable = self.traversables.get(pos)
        if traversable is None:
            traversable = self.get_tile(pos).traversable
            self.traversables[pos] = traversable
        return traversable

    def has_tile(self, pos):
        x, y, z = pos
        return (0 <= x < self.width and 0 <= y < self.height and 0 <= z < len(self.tiles))

    def get_tile(self, pos):
        x, y, z = pos
        return self.tiles[z][y][x]

    def get_events(self, pos):
        tile = self.get_tile(pos)
        if isinstance(tile, Event):
            yield tile
        for e in self.events:
            if (e.x, e.y, e.z) == pos:
                yield e

    def moved(self, game, player, old_pos, new_pos):
        for event in self.get_events(new_pos):
            if hasattr(event, 'cross'):
                event.cross(game, player)
        #print(new_pos, tile)
