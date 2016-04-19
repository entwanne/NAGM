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
        if self.dialogs:
            self.pop_dialogs(True)
        elif self.map:
            self.send(self.map.action, self.map.walk_position(self.position, self.direction))

    def battle_step(self, view):
        beast = view.beast
        #attacks = ((att.name, callback(self.send, view.use, att, beast)) for att in beast.attacks)
        attacks = ((att.name, callback(self.send, view.attack, att)) for att in beast.attacks)
        attacks_cb = callback(Choice.spawn, self, *attacks)
        #bag_items = ((obj.name, callback(self.send, view.use, obj, beast)) for obj in self.bag)
        bag_items = ((obj.name, callback(self.send, view.object, obj, beast)) for obj in self.bag)
        bag_cb = callback(Choice.spawn, self, *bag_items)
        #beasts = ((b.name, callback(self.send, view.use, b, beast)) for b in self.beasts)
        #beasts = ()
        beasts = ((b.name, callback(self.send, view.switch, b)) for b in self.beasts)
        beasts_cb = callback(Choice.spawn, self, *beasts)
        Choice.spawn(self, 'Attack', attacks_cb, 'Bag', bag_cb, 'Beasts', beasts_cb, 'Fuite', callback(self.send, view.exit))

    @property
    def moveable(self):
        return super().moveable and not self.dialogs

    @property
    def dialog(self):
        if self.dialogs:
            return self.dialogs[0]

    def add_dialog(self, dialog):
        self.dialogs.append(dialog)
        self.pop_dialogs()

    def pop_dialogs(self, actioned=False):
        while self.dialogs and (actioned or not self.dialogs[0].persistent):
            actioned = False
            self.send(self.dialogs.pop(0).action)

    @sighandler
    def actioned(self, game, player, map, pos):
        Message.spawn(player, "Hello, I'm {}".format(self.name))
