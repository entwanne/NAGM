from .event import Event

class Character(Event):
    "All characters (can move)"

    __attributes__ = Event.__attributes__ + ('dx', 'dy', 'dialog')

    traversable = False

    def __init__(self, *args, **kwargs):
        Event.__init__(self, *args, **kwargs)
        self.direction = 0, -1
        self.dialog = None

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
        return self.dialog is None

class Trainer(Character):
    "All trainers (playable or not)"

    __attributes__ = Character.__attributes__ + ('battle',)

    def __init__(self, *args, **kwargs):
        Character.__init__(self, *args, **kwargs)
        self.battle = None

    @property
    def moveable(self):
        return self.battle is None and self.dialog is None
