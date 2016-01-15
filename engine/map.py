from .gobject import GObject
from .event import Event

class Map(GObject):
    def __init__(self, size, tiles=(), events=(), zones=()):
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

    def can_move(self, x, y, z):
        if not (0 <= x < self.width and 0 <= y < self.height and 0 <= z < len(self.tiles)):
            return False
        traversable = self.traversables.get((x, y, z))
        if traversable is None:
            traversable = self.tiles[z][y][x].traversable
            self.traversables[x, y, z] = traversable
        return traversable

    def get_events(self, pos):
        x, y, z = pos
        tile = self.tiles[z][y][x]
        if isinstance(tile, Event):
            yield tile
        for e in self.events:
            if (e.x, e.y, e.z) == pos:
                yield e

    def moved(self, player, old_pos, new_pos):
        for event in self.get_events(new_pos):
            if hasattr(event, 'cross'):
                event.cross(player)
        #print(new_pos, tile)
