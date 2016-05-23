from .meta import GObjectMeta
from . import signals
from . import meta

@meta.apply
class GObject(metaclass=GObjectMeta):
    'Base-class for all game objets'

    def __init__(self, **kwargs):
        for key in self.__attributes__:
            setattr(self, key, kwargs.pop(key))
        if kwargs:
            raise TypeError('Unexpected attributes {}'.format(', '.join(kwargs.keys())))

    def set(self, **kwargs):
        'Set attributes on the game object'
        for key, value in kwargs.items():
            if key not in self.__attributes__:
                raise TypeError('Unexpected attribute {}'.format(key))
            setattr(self, key, value)

    def send(self, handler, *args, **kwargs):
        'Send a signal to another game objet'
        signals.send_signal(handler, self, *args, **kwargs)

    def __getstate__(self):
        'Save state of a game objet'
        return {k: getattr(self, k) for k in self.__attributes__}

    def __setstate__(self, state):
        'Load state of a game objet'
        self.__init__(**state)
