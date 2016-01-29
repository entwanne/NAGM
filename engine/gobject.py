from .meta import GObjectMeta
from . import signals
from . import meta

@meta.apply
class GObject(metaclass=GObjectMeta):
    # Attributes of the object
    __attributes__ = ()

    def __init__(self, **kwargs):
        for key in self.__attributes__:
            setattr(self, key, kwargs.pop(key))
        if kwargs:
            raise TypeError('Unexpected attributes {}'.format(', '.join(kwargs.keys())))

    def set(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.__attributes__:
                raise TypeError('Unexpected attribute {}'.format(key))
            setattr(self, key, value)

    def send(self, handler, *args, **kwargs):
        signals.send_signal(handler, self, *args, **kwargs)

    def __getstate__(self):
        return {k: getattr(self, k) for k in self.__attributes__}

    def __setstate__(self, state):
        self.__init__(**state)
