import pyglet
import engine.meta

from .resources import players_texgrid

@engine.meta.register('engine.character.Ghost')
@engine.meta.register('engine.character.Character')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__sprites = ()
        self.__sprites_map = None
        self.__walk_offsets = [0, 1, 0, 2]
        self.__sprite_offset = 0
        self.__calc_sprites_offset(False)

    def move(self, *args, **kwargs):
        old_z = self.z
        ret = super().move(*args, **kwargs)
        if ret and self.sprites:
            for z, sprite in enumerate(self.sprites):
                if self.z != old_z:
                    sprite.group = self.map.groups[self.z+z]
                sprite.set_position(self.x*16, (self.y+self.z+z)*16)
        return ret

    def turn(self, dx, dy):
        olddir = self.direction
        ret = super().turn(dx, dy)
        if ret and self.direction != olddir:
            self.__calc_sprites_offset()
        return ret

    def walk(self):
        ret = super().walk()
        if ret or self.moveable:
            self.__walk_offsets.append(self.__walk_offsets.pop(0))
            self.__calc_sprites_offset()
        return ret

    @property
    def sprites(self):
        if self.map is self.__sprites_map:
            return self.__sprites
        map = self.map
        if map is None:
            self.__sprites = ()
        else:
            self.__sprites = (
                pyglet.sprite.Sprite(
                    players_texgrid[0, self.__sprite_offset],
                    x=self.x*16, y=(self.y+self.z)*16,
                    batch=map.batch, group=map.groups[self.z]),
                pyglet.sprite.Sprite(
                    players_texgrid[1, self.__sprite_offset],
                    x=self.x*16, y=(self.y+self.z+1)*16,
                    batch=map.batch, group=map.groups[self.z + 1]),
            )
        self.__sprites_map = map
        return self.__sprites

    def __calc_sprites_offset(self, update=True):
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
        self.__sprite_offset = off
        sprites = self.sprites
        if update:
            for z, sprite in enumerate(sprites):
                sprite.image = players_texgrid[z, off]
