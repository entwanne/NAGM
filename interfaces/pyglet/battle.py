import pyglet
from nagm.engine.meta import register as metareg
from nagm.engine.signals import sighandler

def get_bar(x, y, k=1.):
    width = int(80 * k)
    vertices = (x, y, x, y + 8, x + width, y + 8, x + width, y)
    colors = (int(255 * (1 - k)), int(255 * k), 0, 0) * 4
    return vertices, colors

@metareg('nagm.engine.battle.Battle')
class _:
    def refresh_ui(self):
        self.__sprites = []
        self.__health_bars = []
        for i, beast in enumerate(self.beasts):
            self.__sprites.append(
                pyglet.sprite.Sprite(
                    beast.family.pyglet_img,
                    x=16*(7*i+2), y=16*(7*i+2),
                    batch=self.batch)
            )
            vertices, colors = get_bar(16*(7*i+2), 16*(7*i+2)+4, beast.hp / beast.max_hp)
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
            x, y, *_ = bar.vertices
            bar.vertices, bar.colors = get_bar(x, y, beast.hp / beast.max_hp)

    def change(self, *args, **kwargs):
        super().change(*args, **kwargs)
        for beast, sprite in zip(self.beasts, self.__sprites):
            sprite.image = beast.family.pyglet_img

    def get_translation(self, window, player):
        return 0, 0

