from .gobject import GObject
from .character import Character
from .object import Object
from . import meta

@meta.apply
class BeastFamily(GObject):
    "Family of a beast: name, type, attacks, etc."

    __attributes__ = ('name', 'type')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

@meta.apply
class Beast(Character):
    "All beasts (can be moving on the map, in their balls, etc.)"

    __attributes__ = ('family', 'name', 'hp', 'attack_coef')

    def __init__(self, **kwargs):
        kwargs.setdefault('name', kwargs['family'].name)
        kwargs.setdefault('hp', 50)
        kwargs.setdefault('attack_coef', 10)
        super().__init__(**kwargs)

    @property
    def ko(self):
        return self.hp == 0

    def attack(self, beast):
        beast.hp = max(beast.hp - self.attack_coef, 0)

@meta.apply
class Beastiary(Object):
    "All catched beasts for a player"

    __attributes__ = ('families', 'beasts')

    def __init__(self, **kwargs):
        kwargs.setdefault('families', []) # found families
        kwargs.setdefault('beasts', []) # catched beasts
        super().__init__(**kwargs)
