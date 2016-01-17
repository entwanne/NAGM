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
        if map.can_move((x, y, z)):
            oldmap = self.map
            old = self.x, self.y, self.z
            self.map = map
            self.x, self.y, self.z = x, y, z
            self.send(self.map.moved, old, (x, y, z))

    def turn(self, dx, dy):
        self.direction = dx, dy

    def walk(self):
        dx, dy = self.direction
        self.move(self.x + dx, self.y + dy)
        self.walking = True

class Trainer(Character):
    "All trainers (playable or not)"
