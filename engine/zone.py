from .gobject import GObject
from .beast import Beast

class WildGroup(GObject):
    """Group of wild beasts (beasts are not instanciated until battle)
    groups can reproduct, move to other zones, etc.
    """
    def __init__(self, family, population=2):
        self.family = family # BeastFamily
        self.population = population # number of beasts in the group (can increase, decrease)

import random, itertools, bisect

class Zone(GObject):
    "Beast zones (where battle can be thrown)"
    def __init__(self, type, groups):
        self.type = type # grass, water, etc.
        self.groups = groups # wild groups

    def random_beast(self):
        weights_acc = list(itertools.accumulate(group.population for group in self.groups))
        x = random.random() * weights_acc[-1]
        family = self.groups[bisect.bisect(weights_acc, x)].family
        return Beast(family)
