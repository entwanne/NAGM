import pyglet

grounds_img = pyglet.image.load('res/sols.png')
grounds_imggrid = pyglet.image.ImageGrid(grounds_img, 50, 12)
grounds_texgrid = pyglet.image.TextureGrid(grounds_imggrid)
trees_img = pyglet.image.load('res/arbres.png')
trees_imggrid = pyglet.image.ImageGrid(trees_img, 50, 12)
trees_texgrid = pyglet.image.TextureGrid(trees_imggrid)
players_img = pyglet.image.load('res/persos.png')
players_imggrid = pyglet.image.ImageGrid(players_img, 2, 12)
players_texgrid = pyglet.image.TextureGrid(players_imggrid)


import engine.meta

@engine.meta.register('engine.event.Event')
class _:
    sprites = ()

@engine.meta.register('engine.character.Character')
class _:
    def __init__(self, *args, **kwargs):
        self._map = None
        self.sprite_offset = 9
        super().__init__(*args, **kwargs)

    def move(self, *args, **kwargs):
        old_z = self.z
        super().move(*args, **kwargs)
        if self.sprites:
            for z, sprite in enumerate(self.sprites):
                if self.z != old_z:
                    sprite.group = self.map.event_groups[self.z+z]
                sprite.set_position(self.x*16, (self.y+self.z+z)*16)

    def turn(self, dx, dy):
        olddir = self.direction
        super().turn(dx, dy)
        if self.direction != olddir:
            if dx > 0:
                off = 0
            elif dx < 0:
                off = 6
            elif dy > 0:
                off = 3
            else:
                off = 9
            self.sprite_offset = off
            for z, sprite in enumerate(self.sprites):
                sprite.image = players_texgrid[z, off]

    @property
    def map(self):
        return self._map
    @map.setter
    def map(self, map):
        if map is self._map:
            return
        self._map = map
        if map is None:
            self.sprites = ()
        else:
            self.sprites = (
                pyglet.sprite.Sprite(
                    players_texgrid[0, self.sprite_offset],
                    x=self.x*16, y=(self.y+self.z)*16,
                    batch=map.batch, group=map.event_groups[self.z]),
                pyglet.sprite.Sprite(
                    players_texgrid[1, self.sprite_offset],
                    x=self.x*16, y=(self.y+self.z+1)*16,
                    batch=map.batch, group=map.event_groups[self.z+1]),
            )


@engine.meta.register('engine.tile.Tile')
class _:
    img = grounds_texgrid[0, 0]
    def refresh(self, map, pos): pass

@engine.meta.register('engine.tile.Grass')
class _:
    img = grounds_texgrid[49, 0]

@engine.meta.register('engine.tile.HighGrass')
class _:
    img = grounds_texgrid[48, 3]

@engine.meta.register('engine.tile.Teleport')
class _:
    img = grounds_texgrid[48, 4]


@engine.meta.register('engine.tile.Tree')
class Tree:
    Y, X = 47, 0
    left = True
    trunk = True
    def refresh(self, map, pos):
        x, y, z = pos
        xtile = map.get_tile((x - 1, y, z))
        if isinstance(xtile, Tree) and xtile.left:
            self.left = False
            self.X += 1
        ytile = map.get_tile((x, y - 1, z))
        if isinstance(ytile, Tree) and ytile.trunk:
            self.trunk = False
            self.Y += 1
        ztile = map.get_tile((x, y, z - 1))
        if isinstance(ztile, Tree):
            if self.trunk:
                self.X, self.Y = 0, 0
            else:
                self.Y += 1

    @property
    def img(self):
        return trees_texgrid[self.Y, self.X]


@engine.meta.register('engine.map.Map')
class _:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.tile_groups = [pyglet.graphics.OrderedGroup(2 * i) for i in range(self.levels)]
        self.event_groups = [pyglet.graphics.OrderedGroup(2 * i + 1) for i in range(self.levels + 1)] # + 1 for heads (superior level)
        print(self.event_groups)

        for z, level in enumerate(self.tiles):
            for y, line in enumerate(level):
                for x, tile in enumerate(line):
                    tile.refresh(self, (x, y, z))
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
        @self.window.event
        def on_key_press(key, modifiers):
            self.key_press(key)
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
        dx = self.window.width // 2 - self.player.sprites[0].x
        dy = self.window.height // 2 - self.player.sprites[0].y
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
                if self.player.direction == (dx, dy):
                    self.player.walk()
                else:
                    self.player.turn(dx, dy)
                self.signals_clock.reset()
                self.keyboard_clock.reset()

    def key_press(self, key):
        if key == pyglet.window.key.SPACE:
            self.player.action()

    def run(self):
        pyglet.app.run()
