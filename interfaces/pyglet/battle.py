import pyglet
import engine.meta
from engine.signals import sighandler

from .beast import textures as beasts_imgs

def get_bar(x, y, k=1.):
    width = int(100 * k)
    vertices = (x, y, x, y + 10, x + width, y + 10, x + width, y)
    colors = (int(255 * (1 - k)), int(255 * k), 0, 0) * 4
    return vertices, colors

@engine.meta.register('engine.battle.Battle')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch = pyglet.graphics.Batch()
        self.__sprites = []
        self.__health_bars = []
        for i, beast in enumerate(self.beasts):
            print(beast)
            if beast and beast.family.name in beasts_imgs:
                self.__sprites.append(
                    pyglet.sprite.Sprite(
                        beasts_imgs[beast.family.name],
                        x=100*i, y=100*i,
                        batch=self.batch)
                )
            vertices, colors = get_bar(100*i, 100*i, beast.hp / beast.max_hp)
            self.__health_bars.append(
                self.batch.add(4,
                               pyglet.gl.GL_QUADS,
                               None,
                               ('v2i', vertices),
                               ('c4B', colors)
                           )
            )

    def attack(self, *args, **kwargs):
        super().attack(*args, **kwargs)
        for beast, bar in zip(self.beasts, self.__health_bars):
            if not beast:
                continue
            x, y, *_ = bar.vertices
            bar.vertices, bar.colors = get_bar(x, y, beast.hp / beast.max_hp)
