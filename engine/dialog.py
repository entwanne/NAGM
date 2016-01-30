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

def spawn_cls(arg, signal=None):
    if isinstance(arg, str):
        return (Message, {'msg': arg, 'signal': signal})
    if isinstance(arg, tuple):
        choices, signals = [], []
        for choice in arg:
            if isinstance(choice, tuple):
                choice, *queue = choice
                sig = spawn_signal(queue, signal)
                choices.append(choice)
                signals.append(sig)
            else:
                choices.append(choice)
                signals.append(signal)
        return (Choice, {'choices': tuple(choices), 'signals': tuple(signals)})
    return (None, None)

def spawn_signal(queue, signal=None):
    for arg in reversed(queue):
        cls, kwargs = spawn_cls(arg, signal)
        if cls:
            dialog = bind._(cls, **kwargs)
            signal = bind.callback(GObject.set, bind._, dialog=dialog)
        else:
            signal = arg
    return signal

def spawn(*args):
    first, *args = args
    signal = spawn_signal(args)
    cls, kwargs = spawn_cls(first, signal)
    if cls:
        return cls(**kwargs)
    raise TypeError
