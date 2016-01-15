import pyglet

window = pyglet.window.Window(width=800, height=600)
@window.event
def on_expose():
    pass

batch = pyglet.graphics.Batch()
sprites = []

grounds_img = pyglet.image.load('res/sols.png')
grounds_imggrid = pyglet.image.ImageGrid(grounds_img, 50, 12)
grounds_texgrid = pyglet.image.TextureGrid(grounds_imggrid)
players_img = pyglet.image.load('res/persos.png')
player_img = players_img.get_region(9 * 16, 0, 16, 32)


import engine.meta

@engine.meta.register('engine.player.Player')
class _:
    def __init__(self, *args, **kwargs):
        self._map = None
        super().__init__(*args, **kwargs)

    def move(self, *args, **kwargs):
        super().move(*args, **kwargs)
        print(self)
        self.sprite.set_position(self.x*16, self.y*16)

    @property
    def map(self):
        return self._map
    @map.setter
    def map(self, value):
        self._map = value


@engine.meta.register('engine.tile.Grass')
class _:
    sprite = grounds_texgrid[49, 0]


@engine.meta.register('engine.tile.HighGrass')
class _:
    sprite = grounds_texgrid[22, 11]


@engine.meta.register('engine.game.Game')
class _:
    def run(self):
        @window.event
        def on_draw():
            dx = window.width // 2 - self.player.sprite.x
            dy = window.height // 2 - self.player.sprite.y
            window.clear()
            pyglet.gl.glTranslatef(dx, dy, 0)
            batch.draw()
            pyglet.gl.glTranslatef(-dx, -dy, 0)

        @window.event
        def on_key_press(key, modifiers):
            if key == pyglet.window.key.LEFT:
                self.player.walk(-1, 0)
            elif key == pyglet.window.key.RIGHT:
                self.player.walk(1, 0)
            elif key == pyglet.window.key.UP:
                self.player.walk(0, 1)
            elif key == pyglet.window.key.DOWN:
                self.player.walk(0, -1)
            self.handle_signals()

        map = self.player.map
        tile_groups = [pyglet.graphics.OrderedGroup(2 * i) for i in range(map.levels)]
        event_groups = [pyglet.graphics.OrderedGroup(2 * i + 1) for i in range(map.levels)]

        for z, level in enumerate(map.tiles):
            for y, line in enumerate(level):
                for x, tile in enumerate(line):
                    if hasattr(tile, 'sprite'):
                        sprites.append(
                            pyglet.sprite.Sprite(
                                tile.sprite,
                                x=x*16, y=(y+z)*16,
                                batch=batch, group=tile_groups[z])
                        )

        self.player.sprite = pyglet.sprite.Sprite(player_img, x=self.player.x*16, y=self.player.y*16, batch=batch, group=event_groups[0])

        pyglet.app.run()
