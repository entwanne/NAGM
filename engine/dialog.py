from .gobject import GObject
from . import meta
from .signals import sighandler

@meta.apply
class Dialog(GObject):
    __attributes__ = ('dest', 'src')

    def __init__(self, **kwargs):
        kwargs.setdefault('src', None)
        super().__init__(**kwargs)
        self.dest.dialog = self
        if self.src is not None:
            self.src.dialog = self

    @sighandler
    def action(self, game, player):
        self.dest.dialog = None
        if self.src is not None:
            self.src.dialog = None

@meta.apply
class Message(Dialog):
    __attributes__ = ('msg',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.msg)

@meta.apply
class Choice(Dialog):
    __attributes__ = ('choices',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.choices)
