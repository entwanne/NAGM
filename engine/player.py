from .character import Trainer
from . import meta
from .dialog import Message, Choice
from .bind import callback
from .signals import sighandler

@meta.apply
class Player(Trainer):
    "Playable trainer(s)"

    __attributes__ = ('name', 'dialogs',)

    def __init__(self, **kwargs):
        kwargs.setdefault('dialogs', [])
        super().__init__(**kwargs)

    def action(self):
        if self.dialog:
            self.send(self.dialog.action)
        elif self.battle:
            self.send(self.battle.action)
        else:
            self.send(self.map.action, self.map.walk_position(self.position, self.direction))

    def battle_step(self, battle, beast):
        attacks = ((att.name, callback(battle.attack, beast, att))
                   for att in beast.attacks)
        choices, signals = zip(*attacks)
        attacks = Choice(choices=choices, signals=signals)
        self.add_dialog(Choice(
            choices=('Attack', 'Fuite'),
            signals=(callback(self.add_dialog, attacks), callback(battle.end))))

    @property
    def moveable(self):
        return super().moveable and not self.dialogs

    @property
    def dialog(self):
        if self.dialogs:
            return self.dialogs[0]

    def add_dialog(self, dialog):
        self.dialogs.append(dialog)

    @sighandler
    def actioned(self, game, player, map, pos):
        player.add_dialog(Message(msg="Hello, I'm {}".format(self.name)))
