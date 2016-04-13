import pyglet
from nagm.engine.meta import register as metareg

from .resources import objects_texgrid

# factorize with Character in Event (__sprites_map, refresh_ui)
@metareg('nagm.engine.object.Object')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__sprites_map = None

    def refresh_ui(self):
        if self.map is None:
            self.sprites = ()
            self.__sprites_map = None
            return
        if self.__sprites_map is not self.map:
            self.sprites = (
                pyglet.sprite.Sprite(
                    objects_texgrid[48, 2],
                    x=self.x*16, y=(self.y+self.z)*16,
                    batch=self.map.batch, group=self.map.groups[self.z])
            )
            self.__sprites_map = self.map
