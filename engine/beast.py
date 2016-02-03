from .gobject import GObject
from .character import Character
from .object import Object
from . import meta
from .attack import lutte

@meta.apply
class BeastFamily(GObject):
    "Family of a beast: name, type, attacks, etc."

    __attributes__ = ('name', 'type', 'attacks')

    def __init__(self, **kwargs):
        kwargs.setdefault('attacks', (lutte,))
        super().__init__(**kwargs)

@meta.apply
class Beast(Character):
    "All beasts (can be moving on the map, in their balls, etc.)"

    __attributes__ = ('family', 'name', 'max_hp', 'hp', 'attacks')

    def __init__(self, **kwargs):
        kwargs.setdefault('name', kwargs['family'].name)
        kwargs.setdefault('max_hp', 50)
        kwargs.setdefault('hp', 50)
        kwargs.setdefault('attacks', list(kwargs['family'].attacks))
        super().__init__(**kwargs)

    @property
    def ko(self):
        return self.hp == 0

    def attack(self, att, beast):
        att.use(self, beast)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(value, 0)

@meta.apply
class Beastiary(Object):
    "All catched beasts for a player"

    __attributes__ = ('families', 'beasts')

    def __init__(self, **kwargs):
        kwargs.setdefault('families', []) # found families
        kwargs.setdefault('beasts', []) # catched beasts
        super().__init__(**kwargs)
