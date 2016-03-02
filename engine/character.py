from .event import Event
from . import event
from . import meta

import random

@meta.apply
class Ghost(Event):
    "Disabled character"

    __attributes__ = ('direction',)

    traversable = False

    def __init__(self, **kwargs):
        kwargs.setdefault('direction', (0, -1))
        super().__init__(**kwargs)

@meta.apply
class Character(Event):
    "All characters (can move)"

    __attributes__ = ('direction', 'ghost')

    traversable = False

    def __init__(self, **kwargs):
        kwargs.setdefault('direction', (0, -1))
        kwargs.setdefault('ghost', None)
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
        if not self.map:
            return False
        return self.move(*self.map.walk_position(self.position, self.direction))

    @property
    def moveable(self):
        return True

    def ghostify(self):
        if self.ghost:
            return
        self.ghost = Ghost(position=self.position, direction=self.direction, map=self.map)
        self.map = None
        event.events.append(self.ghost)

    def pop_ghost(self):
        if not self.ghost:
            return
        ghost, self.ghost = self.ghost, None
        self.map, self.position, self.direction = ghost.map, ghost.position, ghost.direction
        event.events.remove(ghost)

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
        self.send(battle.action, att, beast)
