from engine import *

class BourgChar(character.Character):
    def __init__(self, **kwargs):
        character.Character.__init__(self, **kwargs)
        self.n = 0

    def actioned(self, game, player, map, pos):
        x, y, z = pos
        dx, dy = player.x - x, player.y - y
        self.turn(dx, dy)
        dialog.Dialog(msg='Hello', dest=player, src=self)

    def step(self, game):
        self.n = (self.n + 1) % 5
        if self.n:
            return
        if not self.walk():
            dx, dy = self.direction
            dc = dx + dy * 1j
            dc *= 1j
            dx, dy = int(dc.real), int(dc.imag)
            self.turn(dx, dy)
