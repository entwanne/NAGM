from .gobject import GObject
from .character import Character
from .object import Object

class BeastFamily(GObject):
    "Family of a beast: name, type, attacks, etc."
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Beast(Character):
    "All beasts (can be moving on the map, in their balls, etc.)"
    def __init__(self, family, name=None):
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
    def __init__(self):
        self.families = [] # found families
        self.beasts = [] # catched beasts
