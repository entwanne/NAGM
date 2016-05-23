from .event import Event
from .attack import Useable
from .signals import sighandler
from . import dialog
from . import meta

# object = effects with trainer as sender
# share code with attacks (Useable)
# + methods proper to object (action when found on the map)
# + quantities + player bag

# objects must interact with map to know if they can be used
# example: bicycle, road/city maps will say True, but not battles or houses
# permet aussi de faire des bonus sympas, genre une ball utilisable sur une map normale (qui pourrait servir à attraper un pokémon invisible, hors combat)
# pourrait permettre aussi de lister les pokémons présents sur la map et donc sujets à l'objet (pokéflûte par exemple)

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
        'Find an object on a map'
        dialog.spawn(player, '{} got {}'.format(player.name, self.name))
        self.remove() # remove object from the map
        player.bag.append(self)
