from .event import Event
from .attack import Useable
from .signals import sighandler
from . import dialog
from . import meta

# object = effects with trainer as sender
# share code with attacks (Useable)
# + methods proper to object (action when found on the map)
# + quantities + player bag

@meta.apply
class Object(Useable, Event):
    "All objects (can be found on the map, put in the bag)"

    __attributes__ = ('quantity', 'trashable')

    def __init__(self, **kwargs):
        kwargs.setdefault('quantity', 1)
        kwargs.setdefault('trashable', True)
        return super().__init__(**kwargs)

    @sighandler
    def actioned(self, game, player, map, pos):
        dialog.spawn(player, '{} got {}'.format(player.name, self.name))
        self.remove()
        player.bag.append(self)
