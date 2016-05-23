from .gobject import GObject
from . import meta
from .signals import sighandler
from . import bind

@meta.apply
class Dialog(GObject):
    'Dialogs sent to a player'

    __attributes__ = ('group',)
    persistent = True

    def __init__(self, **kwargs):
        kwargs.setdefault('group', None)
        super().__init__(**kwargs)

    @classmethod
    def spawn(cls, player, **kwargs):
        'Spawn a dialog to a player'
        dialog = cls(**kwargs)
        if dialog.group is not None:
            dialog.group.add(dialog)
        player.add_dialog(dialog)
        return dialog

    @sighandler
    def action(self, game, player):
        'Action executed whn the player closes the dialog'
        if self.group is not None:
            self.group.remove(self)

@meta.apply
class Action(Dialog):
    '''Dialog with a callback
    Actions are not persistent, so they are immediatly closed (callback is called just after the action is spawned)
    '''

    __attributes__ = ('callback',)
    persistent = False

    @classmethod
    def spawn(cls, player, callback, **kwargs):
        return super().spawn(player, callback=callback, **kwargs)

    @sighandler
    def action(self, game, player):
        super().action(game, player)
        self.callback(game, player)

@meta.apply
class Message(Dialog):
    'Dialog with a text message'

    __attributes__ = ('msg',)

    @classmethod
    def spawn(cls, player, msg, **kwargs):
        return super().spawn(player, msg=msg, **kwargs)

@meta.apply
class Choice(Dialog):
    'Choice between several options (each option has a label and a callback)'

    __attributes__ = ('labels', 'callbacks', 'current')

    def __init__(self, **kwargs):
        kwargs.setdefault('current', 0)
        super().__init__(**kwargs)
        if len(self.labels) != len(self.callbacks):
            raise ValueError("labels and callbacks parameters should have same length")

    @classmethod
    def spawn(cls, player, *choices, **kwargs):
        if isinstance(choices[0], str): # 'label1', cb1, 'label2', cb2, ...
            labels, callbacks = choices[::2], choices[1::2]
        else: # ('label1', cb1), ('label2', cb2), ...
            labels, callbacks = zip(*choices)
        return super().spawn(player, labels=labels, callbacks=callbacks, **kwargs)

    @sighandler
    def action(self, game, player):
        super().action(game, player)
        callback = self.callbacks[self.current]
        if callback:
            callback(game, player, self.current)

def spawn(player, *dialogs, group=None):
    'Helper to spawn a message/choice/action'
    for dialog in dialogs:
        if callable(dialog):
            Action.spawn(player, dialog, group=group)
        elif isinstance(dialog, tuple) or isinstance(dialog, list):
            Choice.spawn(player, *dialog, group=group)
        else:
            Message.spawn(player, dialog, group=group)

class DialogGroupSpawner(set):
    'A group is a set of dialogs, used to know which dialogs are active'

    def spawn(self, *args, **kwargs):
        'Spawn a new dialog in this group'
        return spawn(*args, group=self, **kwargs)

    def callback(self, *args, **kwargs):
        'Callback to spawn a dialog in the group'
        return bind.callback(
            self.spawn,
            bind._[1], # player
            *args, **kwargs)
