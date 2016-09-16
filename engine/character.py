from .event import Event
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
    "All characters on a map (moveable events)"

    __attributes__ = ('direction', 'ghost', 'falling')

    traversable = False

    def __init__(self, **kwargs):
        kwargs.setdefault('direction', (0, -1))
        kwargs.setdefault('ghost', None)
        kwargs.setdefault('falling', False)
        super().__init__(**kwargs)

    def move(self, x, y, z=None, map=None):
        'Try to move the character (change position)'
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
        'Try to turn the character (change direction)'
        if not self.moveable:
            return False
        self.direction = dx, dy
        return True

    def walk(self):
        'Try to move character of 1 case in the current direction'
        if not self.map:
            return False
        return self.move(*self.map.walk_position(self.position, self.direction))

    def fall(self):
        'Handle gravity: if there is nothing under the character, it falls'
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
        'Create a ghost of the character'
        if self.ghost:
            return
        self.ghost = Ghost.spawn(position=self.position, direction=self.direction, map=self.map)
        self.map = None

    def pop_ghost(self): # got better name (respawn ?)
        "Delete the character's ghost"
        if not self.ghost:
            return
        ghost, self.ghost = self.ghost, None
        self.map, self.position, self.direction = ghost.map, ghost.position, ghost.direction
        ghost.remove()

@meta.apply
class Trainer(Character):
    "All trainers (playable or not), a Trainer is a Character with beasts"

    __attributes__ = ('beasts', 'bag')

    def __init__(self, **kwargs):
        kwargs.setdefault('beasts', [])
        kwargs.setdefault('bag', [])
        super().__init__(**kwargs)

    def battle_step(self, view):
        'Called each time the trainer has to chose an action'
        att = random.choice(view.beast.attacks)
        self.send(view.attack, att, (view.beast if att.reflexive else view.adv_beast))

    def end_battle(self):
        'End a battle'
        for beast in self.beasts:
            beast.stats.recompute()
        self.pop_ghost() # let Battle do that
