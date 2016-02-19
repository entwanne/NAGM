from .gobject import GObject
from . import meta
from .signals import sighandler
from . import bind

@meta.apply
class Dialog(GObject):
    persistent = True

    @sighandler
    def action(self, game, player):
        pass

@meta.apply
class Action(Dialog):
    __attributes__ = ('callback',)
    persistent = False

    @sighandler
    def action(self, game, player):
        self.callback(game, player)

@meta.apply
class Message(Dialog):
    __attributes__ = ('msg',)

@meta.apply
class Choice(Dialog):
    __attributes__ = ('choices', 'signals', 'current')

    def __init__(self, **kwargs):
        kwargs.setdefault('current', 0)
        super().__init__(**kwargs)
        if len(self.choices) != len(self.signals):
            raise ValueError("choices and signals parameters should have same length")

    @sighandler
    def action(self, game, player):
        super().action(game, player)
        sig = self.signals[self.current]
        if sig:
            self.send(sig, player, self.current)

def spawn(player, *dialogs):
    for dialog in dialogs:
        if not isinstance(dialog, Dialog):
            dialog = Message(msg=dialog)
        player.add_dialog(dialog)
