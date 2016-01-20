from .meta import GObjectMeta
from . import signals

class GObject(metaclass=GObjectMeta):
    def __init__(self):
        pass

    def send(self, handler, *args, **kwargs):
        signals.send_signal(handler, self, *args, **kwargs)
