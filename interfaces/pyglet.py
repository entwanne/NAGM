import pyglet

grounds_img = pyglet.image.load('res/sols.png')
grounds_imggrid = pyglet.image.ImageGrid(grounds_img, 50, 12)
grounds_texgrid = pyglet.image.TextureGrid(grounds_imggrid)
#trees_img = pyglet.image.load('res/arbres.png')
#trees_imggrid = pyglet.image.ImageGrid(trees_img, 50, 12)
#trees_texgrid = pyglet.image.TextureGrid(trees_imggrid)
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
            self.sprite = pyglet.sprite.Sprite(
                player_img,
                x=self.x*16, y=(self.y+self.z)*16,
                batch=map.batch, group=map.event_groups[self.z])


@engine.meta.register('engine.tile.Tile')
class _:
    img = grounds_texgrid[0, 0]

@engine.meta.register('engine.tile.Grass')
class _:
    img = grounds_texgrid[49, 0]

@engine.meta.register('engine.tile.HighGrass')
class _:
    img = grounds_texgrid[48, 3]

@engine.meta.register('engine.tile.Teleport')
class _:
    img = grounds_texgrid[48, 4]


@engine.meta.register('engine.map.Map')
class _:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.tile_groups = [pyglet.graphics.OrderedGroup(2 * i) for i in range(self.levels)]
        self.event_groups = [pyglet.graphics.OrderedGroup(2 * i + 1) for i in range(self.levels)]

        for z, level in enumerate(self.tiles):
            for y, line in enumerate(level):
                for x, tile in enumerate(line):
                    tile.sprite = pyglet.sprite.Sprite(
                        tile.img,
                        x=x*16, y=(y+z)*16,
                        batch=self.batch, group=self.tile_groups[z])


import time
class Clock:
    def __init__(self, max=None):
        self.reset()
        self.max = max
    def reset(self):
        self.time = time.time()
    @property
    def elapsed(self):
        return time.time() - self.time
    @property
    def finished(self):
        if self.max is None:
            return False
        return self.elapsed > self.max

@engine.meta.register('engine.game.Game')
class _:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = pyglet.window.Window(width=800, height=600)
        @self.window.event
        def on_expose():
            pass
        @self.window.event
        def on_draw():
            self.draw()

        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        tick = 0.3
        tick = 0.
        self.signals_clock = Clock(tick)
        self.keyboard_clock = Clock(tick)
        pyglet.clock.schedule(self.update)

    def draw(self):
        if self.player.map is None:
            return
        dx = self.window.width // 2 - self.player.sprite.x
        dy = self.window.height // 2 - self.player.sprite.y
        self.window.clear()
        pyglet.gl.glTranslatef(dx, dy, 0)
        self.player.map.batch.draw()
        pyglet.gl.glTranslatef(-dx, -dy, 0)

    def update(self, _dt):
        if self.have_signals():
            if self.signals_clock.finished:
                self.handle_signals()
                self.signals_clock.reset()
            return
        if self.keyboard_clock.finished:
            dx, dy = 0, 0
            if self.keys.get(pyglet.window.key.LEFT):
                dx = -1
            elif self.keys.get(pyglet.window.key.RIGHT):
                dx = 1
            if self.keys.get(pyglet.window.key.UP):
                dy = 1
            elif self.keys.get(pyglet.window.key.DOWN):
                dy = -1
            if dx or dy:
                self.player.walk(dx, dy)
                self.signals_clock.reset()
                self.keyboard_clock.reset()

    def run(self):
        pyglet.app.run()
