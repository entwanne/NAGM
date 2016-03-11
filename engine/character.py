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

    __attributes__ = ('direction', 'ghost', 'falling')

    traversable = False

    def __init__(self, **kwargs):
        kwargs.setdefault('direction', (0, -1))
        kwargs.setdefault('ghost', None)
        kwargs.setdefault('falling', False)
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
        self.falling = False
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

    def fall(self):
        if self.falling:
            return
        self.falling = True
        self._fall()

    def _fall(self):
        if not self.falling:
            return
        x, y, z = self.position
        if not self.move(x, y, z - 1):
            self.send(self._fall)

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
        ghost.map = None
        event.events.remove(ghost)

@meta.apply
class Trainer(Character):
    "All trainers (playable or not)"

    __attributes__ = ('beasts',)

    def __init__(self, **kwargs):
        kwargs.setdefault('beasts', [])
        super().__init__(**kwargs)

    def battle_step(self, use, beast):
        att = random.choice(beast.attacks)
        self.send(use, att, beast)
