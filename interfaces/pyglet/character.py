import pyglet
from nagm.engine.meta import register as metareg

from .resources import players_texgrid

@metareg('nagm.engine.character.Ghost')
@metareg('nagm.engine.character.Character')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__sprites_map = None
        self.__walk_offsets = [0, 1, 0, 2]

    def refresh_ui(self):
        if self.map is None:
            self.sprites = ()
            self.__sprites_map = None
            return
        dx, dy = self.direction
        if dx > 0:
            off = 0
        elif dx < 0:
            off = 6
        elif dy > 0:
            off = 3
        else:
            off = 9
        off += self.__walk_offsets[0]
        if self.__sprites_map is self.map:
            for z, sprite in enumerate(self.sprites):
                sprite.group = self.map.groups[self.z + z]
                sprite.image = players_texgrid[z, off]
                sprite.set_position(self.x*16, (self.y+self.z+z)*16)
        else:
            self.sprites = (
                pyglet.sprite.Sprite(
                    players_texgrid[0, off],
                    x=self.x*16, y=(self.y+self.z)*16,
                    batch=self.map.batch, group=self.map.groups[self.z]),
                pyglet.sprite.Sprite(
                    players_texgrid[1, off],
                    x=self.x*16, y=(self.y+self.z+1)*16,
                    batch=self.map.batch, group=self.map.groups[self.z + 1]),
            )
            self.__sprites_map = self.map

    def move(self, *args, **kwargs):
        ret = super().move(*args, **kwargs)
        if ret:
            self.invalidate_ui()
        return ret

    def turn(self, dx, dy):
        olddir = self.direction
        ret = super().turn(dx, dy)
        if ret and self.direction != olddir:
            self.invalidate_ui()
        return ret

    def walk(self):
        ret = super().walk()
        if ret or self.moveable:
            self.__walk_offsets.append(self.__walk_offsets.pop(0))
            self.invalidate_ui()
        return ret

    def pop_ghost(self):
        ghost = self.ghost
        super().pop_ghost()
        self.invalidate_ui()
        if ghost:
            ghost.invalidate_ui()
