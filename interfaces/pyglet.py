import pyglet

window = pyglet.window.Window(width=800, height=600)
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
@window.event
def on_expose():
    pass

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
        self.sprite = None
        super().__init__(*args, **kwargs)

    def move(self, *args, **kwargs):
        super().move(*args, **kwargs)
        if self.sprite is not None:
            self.sprite.set_position(self.x*16, self.y*16)

    @property
    def map(self):
        return self._map
    @map.setter
    def map(self, map):
        if map is self._map:
            return
        self._map = map
        if map is None:
            self.sprite = None
        else:
            self.sprite = pyglet.sprite.Sprite(player_img, x=self.x*16, y=self.y*16, batch=map.batch, group=map.event_groups[self.z])


@engine.meta.register('engine.tile.Grass')
class _:
    sprite = grounds_texgrid[49, 0]

@engine.meta.register('engine.tile.HighGrass')
class _:
    sprite = grounds_texgrid[48, 3]

@engine.meta.register('engine.tile.Teleport')
class _:
    sprite = grounds_texgrid[48, 4]


@engine.meta.register('engine.map.Map')
class _:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.tile_groups = [pyglet.graphics.OrderedGroup(2 * i) for i in range(self.levels)]
        self.event_groups = [pyglet.graphics.OrderedGroup(2 * i + 1) for i in range(self.levels)]

        for z, level in enumerate(self.tiles):
            for y, line in enumerate(level):
                for x, tile in enumerate(line):
                    if hasattr(tile, 'sprite'):
                        self.sprites.append(
                            pyglet.sprite.Sprite(
                                tile.sprite,
                                x=x*16, y=(y+z)*16,
                                batch=self.batch, group=self.tile_groups[z])
                        )


import time
class Clock:
    def __init__(self):
        self.reset()
    def reset(self):
        self.time = time.time()
    @property
    def elapsed(self):
        return time.time() - self.time

@engine.meta.register('engine.game.Game')
class _:
    def run(self):
        @window.event
        def on_draw():
            if self.player.map is None:
                return
            dx = window.width // 2 - self.player.sprite.x
            dy = window.height // 2 - self.player.sprite.y
            window.clear()
            pyglet.gl.glTranslatef(dx, dy, 0)
            self.player.map.batch.draw()
            pyglet.gl.glTranslatef(-dx, -dy, 0)

        TICK = 0.3
        signals_clock = Clock()
        keyboard_clock = Clock()
        def update(dt):
            if self.have_signals():
                if signals_clock.elapsed >= TICK:
                    self.handle_signals()
                    signals_clock.reset()
                return
            if keyboard_clock.elapsed >= TICK:
                dx, dy = 0, 0
                if keys.get(pyglet.window.key.LEFT):
                    dx = -1
                if keys.get(pyglet.window.key.RIGHT):
                    dx = 1
                if keys.get(pyglet.window.key.UP):
                    dy = 1
                if keys.get(pyglet.window.key.DOWN):
                    dy = -1
                if dx or dy:
                    self.player.walk(dx, dy)
                    signals_clock.reset()
                    keyboard_clock.reset()
        pyglet.clock.schedule(update)

        pyglet.app.run()
