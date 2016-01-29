from .gobject import GObject
from . import meta
from .signals import sighandler
from . import bind

@meta.apply
class Dialog(GObject):
    __attributes__ = ()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @sighandler
    def action(self, game, player):
        player.dialog = None

@meta.apply
class Message(Dialog):
    __attributes__ = ('msg', 'signal')

    def __init__(self, **kwargs):
        kwargs.setdefault('signal', None)
        super().__init__(**kwargs)
        print(self.msg)

    @sighandler
    def action(self, game, player):
        super().action(game, player)
        if self.signal:
            self.send(self.signal, player)

@meta.apply
class Choice(Dialog):
    __attributes__ = ('choices',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.choices)

def spawn_messages(*messages, signal=None):
    first, *messages = messages
    for msg in reversed(messages):
        cmsg = bind._(Message, msg=msg, signal=signal)
        signal = bind.callback(GObject.set, bind._, dialog=cmsg)
    return Message(msg=first, signal=signal)
