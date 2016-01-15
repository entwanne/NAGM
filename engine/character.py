from .event import Event

class Character(Event):
    "All characters (can move)"
    traversable = False

    def move(self, x, y, z=None):
        if z is None:
            z = self.z
        if self.map.can_move(x, y, z):
            old = self.x, self.y, self.z
            self.x, self.y, self.z = x, y, z
            self.send('moved', self, self.map, old, (x, y, z))

    def walk(self, dx, dy):
        self.move(self.x + dx, self.y + dy)

class Trainer(Character):
    "All trainers (playable or not)"
