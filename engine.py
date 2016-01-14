signals = [] # queue of signals to handle
handlers = {}
def reg_signal(sigtype, callback):
    handlers.setdefault(sigtype, []).append(callback)
def handle_signals():
    while signals:
        sigtype, *params = signals.pop(0)
        for handler in handlers.get(sigtype, ()):
            handler(sigtype, *params)

class Event:
    "All objects that can interact with player (on the map)"
    def __init__(self):
        self.x, self.y, self.z = 0, 0, 0
        self.map = None

class Character(Event):
    "All characters (can move)"
    traversable = False

    def move(self, x, y, z=None):
        if z is None:
            z = self.z
        if self.map.can_move(x, y, z):
            old = self.x, self.y, self.z
            self.x, self.y, self.z = x, y, z
            signals.append(('moved', self, self.map, old, (x, y, z)))

    def walk(self, dx, dy):
        self.move(self.x + dx, self.y + dy)

class Trainer(Character):
    "All trainers (playable or not)"

class Player(Trainer):
    "Playable trainer(s)"

class Object(Event):
    "All objects (can be found on the map, put in the bag)"

class BeastFamily:
    "Family of a beast: name, type, attacks, etc."

class Beast(Character, BeastFamily):
    "All beasts (can be moving on the map, in their balls, etc.)"

class Beastiary(Object):
    "All catched beasts for a player"
    def __init__(self):
        self.families = [] # found families
        self.beasts = [] # catched beasts

class Tile:
    """All tiles ("voxels") on a map
    have some properties: traversable, etc.
    """

class EventTile(Event, Tile):
    "Tiles that interact with player (stairs)"

class WildGroup:
    """Group of wild beasts (beasts are not instanciated until battle)
    groups can reproduct, move to other zones, etc.
    """
    def __init__(self, family, population=2):
        self.family = family # BeastFamily
        self.population = population # number of beasts in the group (can increase, decrease)

class Zone:
    "Beast zones (where battle can be thrown)"
    def __init__(self, type):
        self.type = type # grass, water, etc.
        self.groups = [] # wild groups

class Map:
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

class Game:
    def __init__(self):
        self.maps = []
        self.player = None

game = Game()

pikachu = BeastFamily()
pikachu.name = 'Pikachu'
pikachu.type = 'Electrik'

pikagroup = WildGroup(pikachu, 10) # group of 10 pikachus
pikazone = Zone('grass')
pikazone.groups = [pikagroup]

class Grass(Tile):
    "Normal grass"
    traversable = True
class HighGrass(EventTile):
    "High grass (battles)"
    traversable = True
    def __init__(self, zone):
        self.zone = zone

bourg = Map(5, 5)
bourg.zones = [pikazone]
bourg.tiles = (
    (
        (Grass(), Grass(), Grass(), Grass(), Grass()),
        (Grass(), HighGrass(pikazone), HighGrass(pikazone), HighGrass(pikazone), Grass()),
        (Grass(), HighGrass(pikazone), HighGrass(pikazone), HighGrass(pikazone), Grass()),
        (Grass(), HighGrass(pikazone), HighGrass(pikazone), HighGrass(pikazone), Grass()),
        (Grass(), Grass(), Grass(), Grass(), Grass()),
    ),
) # event tiles are automatically put in bourg.events
for z, level in enumerate(bourg.tiles):
    for y, line in enumerate(level):
        for x, tile in enumerate(line):
            tile.x, tile.y, tile.z = x, y, z
bourg.events += [Character(), Trainer(), Object()]
bourg.levels = len(bourg.tiles)
game.maps.append(bourg)

player = Player()
player.map = bourg
player.position = (0, 0)
player.beastiary = Beastiary()
game.player = player

reg_signal('moved', lambda _, char, map, old, new: map.moved(char, old, new))

if __name__ == '__main__':
    #handlers['moved'] = [lambda _, char, map, old, new: map.moved(char, old, new)]
    # game:
    player.walk(1, 0) # go to right
    handle_signals()
    player.walk(0, 1) # go up
    handle_signals()
    player.walk(0, 1) # go up
    handle_signals()
    # -> battle
