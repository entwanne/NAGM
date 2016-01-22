from .gobject import GObject
from .character import Character
from .object import Object

class BeastFamily(GObject):
    "Family of a beast: name, type, attacks, etc."

    __attributes__ = GObject.__attributes__ + ('name', 'type')

    def __init__(self, name, type):
        self.name = name
        self.type = type

class Beast(Character):
    "All beasts (can be moving on the map, in their balls, etc.)"

    __attributes__ = Character.__attributes__ + ('family', 'name', 'hp', 'attack_coef')

    def __init__(self, family, name=None):
        Character.__init__(self)
        self.family = family
        if name is None:
            self.name = self.family.name
        else:
            self.name = name
        self.hp = 50
        self.attack_coef = 10

    @property
    def ko(self):
        return self.hp == 0

    def attack(self, beast):
        beast.hp = max(beast.hp - self.attack_coef, 0)

class Beastiary(Object):
    "All catched beasts for a player"

    __attributes__ = GObject.__attributes__ + ('families', 'beasts')

    def __init__(self):
        self.families = [] # found families
        self.beasts = [] # catched beasts
