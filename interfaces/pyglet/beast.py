import pyglet
from nagm.engine.meta import register as metareg
import nagm.engine.resources as res

@metareg('nagm.engine.beast.BeastFamily')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pyglet_img = pyglet.image.load(res.get('beasts/{}.png'.format(self.id)))
