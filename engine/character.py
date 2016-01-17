from .event import Event

class Character(Event):
    "All characters (can move)"
    traversable = False

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.direction = 0, -1

    def move(self, x, y, z=None, map=None):
        self.walking = False
        if z is None:
            z = self.z
        if map is None:
            map = self.map
        pos = x, y, z
        if map.can_move(pos):
            oldmap = self.map
            old = self.position
            self.map = map
            self.position = pos
            self.send(self.map.moved, old, pos)

    def turn(self, dx, dy):
        self.direction = dx, dy

    def walk(self):
        self.move(self.x + self.dx, self.y + self.dy)
        self.walking = True

    @property
    def direction(self):
        return (self.dx, self.dy)

    @direction.setter
    def direction(self, dir):
        self.dx, self.dy = dir

class Trainer(Character):
    "All trainers (playable or not)"
