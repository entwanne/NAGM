from .gobject import GObject
from .character import Character
from .object import Object
from . import meta

@meta.apply
class BeastFamily(GObject):
    "Family of a beast: name, type, attacks, etc."

    __attributes__ = ('id', 'name', 'type', 'hp', 'att', 'dfse', 'attacks')

    def __init__(self, **kwargs):
        if not kwargs['attacks']:
            raise ValueError('BeastFamily should be initialized with at least one attack')
        kwargs.setdefault('hp', 50)
        kwargs.setdefault('att', 1)
        kwargs.setdefault('dfse', 1)
        super().__init__(**kwargs)

@meta.apply
class Beast(Character):
    "All beasts (can be moving on the map, in their balls, etc.)"

    __attributes__ = ('family', 'name', 'max_hp', 'hp', 'att', 'dfse', 'attacks')

    @classmethod
    def from_family(cls, family, **kwargs):
        kwargs['family'] = family
        kwargs.setdefault('name', family.name)
        kwargs.setdefault('max_hp', family.hp)
        kwargs.setdefault('hp', family.hp)
        kwargs.setdefault('att', family.att)
        kwargs.setdefault('dfse', family.dfse)
        kwargs.setdefault('attacks', list(family.attacks))
        return cls(**kwargs)

    @property
    def ko(self):
        return self.hp == 0

    def attack(self, att, beast):
        att.use(self, beast)

    def damages(self, hp):
        self.hp = max(self.hp - hp, 0)

@meta.apply
class Beastiary(Object):
    "All catched beasts for a player"

    __attributes__ = ('families', 'beasts')

    def __init__(self, **kwargs):
        kwargs.setdefault('families', []) # found families
        kwargs.setdefault('beasts', []) # catched beasts
        super().__init__(**kwargs)
