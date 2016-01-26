import pyglet
import engine.meta

@engine.meta.register('engine.map.Map')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch = pyglet.graphics.Batch()
        self.tile_groups = [pyglet.graphics.OrderedGroup(2 * i) for i in range(self.levels)]
        self.event_groups = [pyglet.graphics.OrderedGroup(2 * i + 1) for i in range(self.levels + 1)] # + 1 for heads (superior level)

        for z, level in enumerate(self.tiles):
            for y, line in enumerate(level):
                for x, tile in enumerate(line):
                    tile.refresh(self, (x, y, z))
                    tile.sprite = pyglet.sprite.Sprite(
                        tile.img,
                        x=x*16, y=(y+z)*16,
                        batch=self.batch, group=self.tile_groups[z])
