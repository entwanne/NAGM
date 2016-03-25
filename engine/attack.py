from .gobject import GObject
from . import meta

@meta.apply
class Attack(GObject):
    __attributes__ = ('name', 'type', 'reflexive', 'effects')

    def __init__(self, **kwargs):
        kwargs.setdefault('reflexive', False)
        kwargs.setdefault('effects', ())
        return super().__init__(**kwargs)

    def use(self, sender, target):
        print('{} uses {}'.format(sender.name, self.name))
        for effect in self.effects:
            if not effect(self, sender, target):
                break
