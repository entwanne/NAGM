from .gobject import GObject
from .event import Event

class Map(GObject):
    def __init__(self, size, tiles, zones=()):
        self.width, self.height, self.levels = size
        self.tiles = tiles # map tiles (grounds)
        self.zones = zones # map zones (battles are thrown by events)
        self.events = [] # map events (objects, characters, event tiles, etc.)
        self.neighboars = {} # neighboar maps (for coalescing)
        self.traversables = {}

    @classmethod
    def from_tiles(cls, tiles, zones=()):
        levels = len(tiles)
        height = len(tiles[0]) if levels else 0
        width = len(tiles[0][0]) if height else 0
        return cls((width, height, levels), tiles, zones)

    def can_move(self, pos):
        if not self.has_tile(pos):
            return False
        traversable = self.traversables.get(pos)
        if traversable is None:
            for obj in self.on_case(pos):
                traversable = obj.traversable
            self.traversables[pos] = traversable
        return traversable

    def has_tile(self, pos):
        x, y, z = pos
        return (0 <= x < self.width and 0 <= y < self.height and 0 <= z < len(self.tiles))

    def get_tile(self, pos):
        if not self.has_tile(pos):
            return
        x, y, z = pos
        return self.tiles[z][y][x]

    def add_event(self, event):
        event.map = self
        self.events.append(event)

    def get_events(self, pos):
        for e in self.events:
            if e.position == pos:
                yield e

    def on_case(self, pos):
        tile = self.get_tile(pos)
        if tile:
            yield tile
        yield from self.get_events(pos)

    def moved(self, game, player, old_map, old_pos, pos):
        for event in self.on_case(pos):
            if hasattr(event, 'crossed'):
                event.crossed(game, player, old_map, old_pos, self, pos)

    def action(self, game, player, pos):
        for event in self.on_case(pos):
            if hasattr(event, 'actioned'):
                event.actioned(game, player, self, pos)
