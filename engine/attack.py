from .gobject import GObject
from . import meta

@meta.apply
class Useable(GObject):
    '''A Useable is an object that can be used (on the map, in a battle)
    It has several effects that are applied each time the useable is used
    '''

    __attributes__ = ('name', 'effects')

    def __init__(self, **kwargs):
        kwargs.setdefault('effects', ())
        return super().__init__(**kwargs)

    def use(self, sender, target):
        '''Apply effects on target, stop when an effect returns False
        sender contains the trainer/beast that use the useable
        '''
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
    'An Attack is a Useable that have a type and can be reflexive (target = sender)'
    __attributes__ = ('type', 'reflexive')

    def __init__(self, **kwargs):
        kwargs.setdefault('reflexive', False)
        return super().__init__(**kwargs)
