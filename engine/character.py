from .event import Event

class Character(Event):
    "All characters (can move)"
    traversable = False

    def move(self, x, y, z=None, map=None):
        self.walking = False
        if z is None:
            z = self.z
        if map is None:
            map = self.map
        if map.can_move(x, y, z):
            oldmap = self.map
            old = self.x, self.y, self.z
            self.map = map
            self.x, self.y, self.z = x, y, z
            self.send('moved', self, oldmap, map, old, (x, y, z))

    def walk(self, dx, dy):
        self.move(self.x + dx, self.y + dy)
        self.walking = True

class Trainer(Character):
    "All trainers (playable or not)"
