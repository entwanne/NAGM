import pyglet
import engine.meta

from .resources import players_texgrid

@engine.meta.register('engine.character.Ghost')
@engine.meta.register('engine.character.Character')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sprites = ()
        self.sprites_map = None
        self.calc_sprite_offset(*self.direction)
        self.sprites # compute sprites

    def move(self, *args, **kwargs):
        old_z = self.z
        ret = super().move(*args, **kwargs)
        if ret and self.sprites:
            for z, sprite in enumerate(self.sprites):
                if self.z != old_z:
                    sprite.group = self.map.event_groups[self.z+z]
                sprite.set_position(self.x*16, (self.y+self.z+z)*16)
        return ret

    def turn(self, dx, dy):
        olddir = self.direction
        ret = super().turn(dx, dy)
        if ret and self.direction != olddir:
            self.calc_sprite_offset(dx, dy)
            for z, sprite in enumerate(self.sprites):
                sprite.image = players_texgrid[z, self.sprite_offset]
        return ret

    @property
    def sprites(self):
        if self.map is self.sprites_map:
            return self._sprites
        map = self.map
        if map is None:
            self._sprites = ()
        else:
            self._sprites = (
                pyglet.sprite.Sprite(
                    players_texgrid[0, self.sprite_offset],
                    x=self.x*16, y=(self.y+self.z)*16,
                    batch=map.batch, group=map.event_groups[self.z]),
                pyglet.sprite.Sprite(
                    players_texgrid[1, self.sprite_offset],
                    x=self.x*16, y=(self.y+self.z+1)*16,
                    batch=map.batch, group=map.event_groups[self.z+1]),
            )
        self.sprites_map = map
        return self._sprites

    def calc_sprite_offset(self, dx, dy):
        if dx > 0:
            off = 0
        elif dx < 0:
            off = 6
        elif dy > 0:
            off = 3
        else:
            off = 9
        self.sprite_offset = off
