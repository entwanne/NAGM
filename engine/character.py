from .event import Event
from . import meta

import random

@meta.apply
class Character(Event):
    "All characters (can move)"

    __attributes__ = ('direction',)

    traversable = False

    def __init__(self, **kwargs):
        kwargs.setdefault('direction', (0, -1))
        super().__init__(**kwargs)

    def move(self, x, y, z=None, map=None):
        if not self.moveable:
            return False
        if z is None:
            z = self.z
        if map is None:
            map = self.map
        pos = x, y, z
        if not map.can_move(pos):
            return False
        oldmap = self.map
        old = self.position
        self.map = map
        self.position = pos
        self.send(self.map.moved, oldmap, old, pos)
        return True

    def turn(self, dx, dy):
        if not self.moveable:
            return False
        self.direction = dx, dy
        return True

    def walk(self):
        return self.move(*self.map.walk_position(self.position, self.direction))

    @property
    def direction(self):
        return (self.dx, self.dy)

    @direction.setter
    def direction(self, dir):
        self.dx, self.dy = dir

    @property
    def moveable(self):
        return True

@meta.apply
class Trainer(Character):
    "All trainers (playable or not)"

    __attributes__ = ('battle',)
    __attributes__ += ('beast',) # to delete

    def __init__(self, **kwargs):
        kwargs.setdefault('battle', None)
        kwargs.setdefault('beast', None) # to delete
        super().__init__(**kwargs)

    @property
    def moveable(self):
        return super().moveable and self.battle is None

    def battle_step(self, battle, beast):
        att = random.choice(beast.attacks)
        self.send(battle.attack, beast, att)
