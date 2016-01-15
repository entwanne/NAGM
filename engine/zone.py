from .gobject import GObject

class WildGroup(GObject):
    """Group of wild beasts (beasts are not instanciated until battle)
    groups can reproduct, move to other zones, etc.
    """
    def __init__(self, family, population=2):
        self.family = family # BeastFamily
        self.population = population # number of beasts in the group (can increase, decrease)

class Zone(GObject):
    "Beast zones (where battle can be thrown)"
    def __init__(self, type):
        self.type = type # grass, water, etc.
        self.groups = [] # wild groups
