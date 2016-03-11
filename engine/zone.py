from .gobject import GObject
from .beast import Beast
from . import meta

@meta.apply
class WildGroup(GObject):
    """Group of wild beasts (beasts are not instanciated until battle)
    groups can reproduct, move to other zones, etc.
    """

    __attributes__ = ('family', 'population')

    def __init__(self, **kwargs):
        kwargs.setdefault('population', 2)
        #self.family = family # BeastFamily
        #self.population = population # number of beasts in the group (can increase, decrease)
        super().__init__(**kwargs)

import random, itertools, bisect

@meta.apply
class Zone(GObject):
    "Beast zones (where battle can be thrown)"

    __attributes__ = ('type', 'groups', 'area')

    def __init__(self, **kwargs):
        #self.type = type # grass, water, etc.
        #self.groups = groups # wild groups
        kwargs.setdefault('area', 0)
        super().__init__(**kwargs)

    def random_beast(self):
        weights_acc = list(itertools.accumulate(group.population for group in self.groups))
        x = random.random() * weights_acc[-1]
        family = self.groups[bisect.bisect(weights_acc, x)].family
        return Beast.from_family(family)

    def maybe_beast(self):
        density = sum(group.population for group in self.groups) / self.area if self.area else 0
        if random.random() > density:
            return
        return self.random_beast()
