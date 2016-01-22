from .meta import GObjectMeta
from . import signals

class GObject(metaclass=GObjectMeta):
    # Attributes of the object (owned by this object)
    __attributes__ = ()
    # Other objects linked to this one
    __dependencies__ = ()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.__attributes__:
                raise TypeError('Unexpected attribute {}'.format(key))
            setattr(self, key, value)

    def send(self, handler, *args, **kwargs):
        signals.send_signal(handler, self, *args, **kwargs)
