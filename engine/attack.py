from .gobject import GObject
from . import meta

@meta.apply
class Useable(GObject):
    __attributes__ = ('name', 'effects')

    def __init__(self, **kwargs):
        kwargs.setdefault('effects', ())
        return super().__init__(**kwargs)

    def use(self, sender, target):
        print('{} uses {}'.format(sender.name, self.name))
        for effect in self.effects:
            # effects may have access to target trainer (to force a beast to join the battle for example)
            # and to battle view ? (switch a beast)
            # or use an exception ? beast-switching must cancel other actions
            # + how to pass battle view to exception ?
            if not effect(self, sender, target):
                break

@meta.apply
class Attack(Useable):
    __attributes__ = ('type', 'reflexive')

    def __init__(self, **kwargs):
        kwargs.setdefault('reflexive', False)
        return super().__init__(**kwargs)

    def use(self, sender, target):
        print('{} uses {}'.format(sender.name, self.name))
        for effect in self.effects:
            if not effect(self, sender, target):
                break
