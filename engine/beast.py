from .gobject import GObject
from .character import Character
from .object import Object
from .stats import Stats
from . import meta

@meta.apply
class BeastFamily(GObject):
    "Family of a beast: name, type, attacks, etc."

    __attributes__ = ('id', 'name', 'type', 'stats_ref', 'attacks')

    def __init__(self, **kwargs):
        if not kwargs['attacks']:
            raise ValueError('BeastFamily should be initialized with at least one attack')
        super().__init__(**kwargs)

@meta.apply
class Beast(Character):
    "All beasts (can be moving on the map, in their balls, etc.)"

    __attributes__ = ('family', 'name', 'stats', 'attacks')

    @classmethod
    def from_family(cls, family, **kwargs):
        kwargs['family'] = family
        kwargs.setdefault('name', family.name)
        kwargs.setdefault('stats', family.stats_ref.stats())
        kwargs.setdefault('attacks', list(family.attacks))
        return cls(**kwargs)

    @property
    def id(self):
        return self.family.id

    @property
    def type(self):
        return self.family.type

    @property
    def ko(self):
        return self.stats.hp == 0

    def attack(self, att, target):
        return att.use(self, target)

@meta.apply
class Beastiary(Object):
    "All catched beasts for a player"

    __attributes__ = ('families', 'beasts')

    def __init__(self, **kwargs):
        kwargs.setdefault('families', []) # found families
        kwargs.setdefault('beasts', []) # catched beasts
        super().__init__(**kwargs)
