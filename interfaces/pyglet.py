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

beasts_imgs = {
    'Pikachu': grounds_texgrid[45, 4],
    'Carapuce': grounds_texgrid[45, 7],
}

import engine.meta

@engine.meta.register('engine.event.Event')
class _:
    sprites = ()

@engine.meta.register('engine.character.Character')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sprites = ()
        self.sprites_map = None
        self.calc_sprite_offset(self.dx, self.dy)
        self.sprites # compute sprites

    def move(self, *args, **kwargs):
        old_z = self.z
        ret = super().move(*args, **kwargs)
        if ret and self.sprites:
            for z, sprite in enumerate(self.sprites):
                if self.z != old_z:
                    sprite.group = self.map.event_groups[self.z+z]
                sprite.set_position(self.x*16, (self.y+self.z+z)*16)
        return ret

    def turn(self, dx, dy):
        olddir = self.direction
        ret = super().turn(dx, dy)
        if ret and self.direction != olddir:
            self.calc_sprite_offset(dx, dy)
            for z, sprite in enumerate(self.sprites):
                sprite.image = players_texgrid[z, self.sprite_offset]
        return ret

    @property
    def sprites(self):
        if self.map is self.sprites_map:
            return self._sprites
        map = self.map
        if map is None:
            self._sprites = ()
        else:
            self._sprites = (
                pyglet.sprite.Sprite(
                    players_texgrid[0, self.sprite_offset],
                    x=self.x*16, y=(self.y+self.z)*16,
                    batch=map.batch, group=map.event_groups[self.z]),
                pyglet.sprite.Sprite(
                    players_texgrid[1, self.sprite_offset],
                    x=self.x*16, y=(self.y+self.z+1)*16,
                    batch=map.batch, group=map.event_groups[self.z+1]),
            )
        self.sprites_map = map
        return self._sprites

    def calc_sprite_offset(self, dx, dy):
        if dx > 0:
            off = 0
        elif dx < 0:
            off = 6
        elif dy > 0:
            off = 3
        else:
            off = 9
        self.sprite_offset = off


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

@engine.meta.register('engine.tile.Rock')
class _:
    img = grounds_texgrid[32, 1]

@engine.meta.register('engine.tile.Stairs')
class Stairs:
    img = grounds_texgrid[49, 0]
    def refresh(self, map, pos):
        x, y, z = pos
        if (0, 1) in self.directions:
            self.img = grounds_texgrid[49, 7]


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


@engine.meta.register('engine.dialog.Dialog')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = pyglet.text.Label(self.msg)


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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = pyglet.window.Window(width=21*16, height=21*16)
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
        self.events_clock = Clock(tick)
        #pyglet.clock.schedule(self.update)
        pyglet.clock.schedule_interval(self.update, 0.1)

    def draw(self):
        self.window.clear()
        if self.player.battle:
            self.player.battle.batch.draw()
        elif self.player.map:
            sprite = self.player.sprites[0]
            dx = (self.window.width - sprite.width) // 2 - sprite.x
            dy = (self.window.height - sprite.height) // 2 - sprite.y
            pyglet.gl.glTranslatef(dx, dy, 0)
            self.player.map.batch.draw()
            pyglet.gl.glTranslatef(-dx, -dy, 0)
        if self.player.dialog:
            self.player.dialog.label.draw()

    def update(self, _dt):
        if self.have_signals():
            if self.signals_clock.finished:
                self.handle_signals()
                self.signals_clock.reset()
            return
        if self.events_clock.finished:
            for event in self.events:
                if event.map == self.player.map and hasattr(event, 'step'):
                    event.step(self)
            self.events_clock.reset()
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
        elif key == pyglet.window.key.S:
            self.save('game.save')


    def run(self):
        pyglet.app.run()
