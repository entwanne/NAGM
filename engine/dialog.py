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
        player.dialogs.remove(self)

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
    __attributes__ = ('choices', 'signals', 'current')

    def __init__(self, **kwargs):
        kwargs.setdefault('current', 0)
        super().__init__(**kwargs)
        if len(self.choices) != len(self.signals):
            raise ValueError("choices and signals parameters should have same length")
        print(self.choices)

    @sighandler
    def action(self, game, player):
        super().action(game, player)
        sig = self.signals[self.current]
        if sig:
            self.send(sig, player)

def spawn(player, *dialogs, signal=None):
    *dialogs, last = dialogs
    for dialog in dialogs:
        player.add_dialog(Message(msg=dialog))
    player.add_dialog(Message(msg=last, signal=signal))

def spawn_choice(player, *choices, signal=None):
    choices = ((c, None) if isinstance(c, str) else c for c in choices)
    choices, signals = zip(*choices)
    player.add_dialog(Choice(choices=choices, signals=signals))
