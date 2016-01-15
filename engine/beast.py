from .gobject import GObject
from .character import Character
from .object import Object

class BeastFamily(GObject):
    "Family of a beast: name, type, attacks, etc."

class Beast(Character, BeastFamily):
    "All beasts (can be moving on the map, in their balls, etc.)"

class Beastiary(Object):
    "All catched beasts for a player"
    def __init__(self):
        self.families = [] # found families
        self.beasts = [] # catched beasts
