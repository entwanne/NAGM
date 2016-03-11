import pyglet
import engine.meta

class GroupsDict(dict):
    "Dynamically add groups"
    def __missing__(self, key):
        group = pyglet.graphics.OrderedGroup(key)
        self[key] = group
        return group

@engine.meta.register('engine.map.BaseMap')
class _:
    groups = GroupsDict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch = pyglet.graphics.Batch()

@engine.meta.register('engine.map.Map')
class _:
    def refresh_ui(self):
        for z, level in enumerate(self.tiles):
            for y, line in enumerate(level):
                for x, tile in enumerate(line):
                    tile.refresh(self, (x, y, z))
                    if tile.img is None:
                        continue
                    tile.sprite = pyglet.sprite.Sprite(
                        tile.img,
                        x=x*16, y=(y+z)*16,
                        batch=self.batch,
                        group=self.groups[z - 0.1]) # just under events of the same level

    def get_translation(self, window, player):
        sprite = player.sprites[0]
        dx = (window.width - sprite.width) // 2 - sprite.x
        dy = (window.height - sprite.height) // 2 - sprite.y
        return dx, dy
