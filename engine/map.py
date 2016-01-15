from .gobject import GObject

class Map(GObject):
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.tiles = [] # map tiles (grounds)
        self.events = [] # map events (objects, characters, event tiles, etc.)
        self.zones = [] # map zones (battles are thrown by events)
        self.neighboars = {} # neighboar maps (for coalescing)
        self.traversables = {}
        self.levels = 0

    def can_move(self, x, y, z):
        if not (0 <= x < self.width and 0 <= y < self.height and 0 <= z < len(self.tiles)):
            return False
        traversable = self.traversables.get((x, y, z))
        if traversable is None:
            traversable = self.tiles[z][y][x].traversable
            self.traversables[x, y, z] = traversable
        return traversable

    def moved(self, char, old_pos, new_pos):
        print(new_pos)
