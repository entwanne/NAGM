import pyglet
import engine.meta

from .beast import textures as beasts_imgs

@engine.meta.register('engine.battle.Battle')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch = pyglet.graphics.Batch()
        if self.beasts[1] and self.beasts[1].family.name in beasts_imgs:
            self.sprite = pyglet.sprite.Sprite(
                beasts_imgs[self.beasts[1].family.name],
                x=100, y=100,
                batch=self.batch)
