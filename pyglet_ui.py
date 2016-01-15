#!/usr/bin/env python3

import pyglet

import engine.meta
def my_new(cls, name, bases, dict, decorated=False):
    c = type.__new__(cls, name, bases, dict)
    if decorated:
        return c
    print(cls, c, '{}.{}'.format(c.__module__, c.__qualname__))
    def getattribute(self, name):
        return c.__getattribute__(self, name)
    return engine.meta.GObjectMeta(name,
                                  (c,),
                                  {'__getattribute__': getattribute},
                                  True)
def my_init(cls, name, bases, dict, decorated=False):
    type.__init__(cls, name, bases, dict)
engine.meta.GObjectMeta.__new__ = my_new
engine.meta.GObjectMeta.__init__ = my_init

import engine
from init_game import game

window = pyglet.window.Window(width=800, height=600)

batch = pyglet.graphics.Batch()
tile_groups = [pyglet.graphics.OrderedGroup(2 * i) for i in range(game.maps[0].levels)]
event_groups = [pyglet.graphics.OrderedGroup(2 * i + 1) for i in range(game.maps[0].levels)]

grounds_img = pyglet.image.load('res/sols.png')
grounds_imggrid = pyglet.image.ImageGrid(grounds_img, 50, 12)
grounds_texgrid = pyglet.image.TextureGrid(grounds_imggrid)

tiles_img = {
    engine.tile.Grass: grounds_texgrid[49, 0],
    engine.tile.HighGrass: grounds_texgrid[22, 11],
}
sprites = []
for z, level in enumerate(game.maps[0].tiles):
    for y, line in enumerate(reversed(level)):
        for x, tile in enumerate(line):
            if type(tile) in tiles_img:
                sprites.append(
                    pyglet.sprite.Sprite(
                        tiles_img[type(tile)],
                        x=x*16, y=(y+z)*16,
                        batch=batch, group=tile_groups[z])
                )


players_img = pyglet.image.load('res/persos.png')
player_img = players_img.get_region(9 * 16, 0, 16, 32)
player_sprite = pyglet.sprite.Sprite(player_img, x=game.player.x*16, y=game.player.y*16, batch=batch, group=event_groups[0])

def player_move(_, p, _1, _2, pos):
    if p is not game.player:
        return
    x, y, _ = pos
    player_sprite.set_position(x*16, y*16)
engine.signals.reg_signal('moved', player_move)

@window.event
def on_draw():
    dx = window.width // 2 - player_sprite.x
    dy = window.height // 2 - player_sprite.y
    window.clear()
    pyglet.gl.glTranslatef(dx, dy, 0)
    batch.draw()
    pyglet.gl.glTranslatef(-dx, -dy, 0)

@window.event
def on_expose():
    pass

@window.event
def on_key_press(key, modifiers):
    if key == pyglet.window.key.LEFT:
        #player.x -= 16
        game.player.walk(-1, 0)
    elif key == pyglet.window.key.RIGHT:
        #player.x += 16
        game.player.walk(1, 0)
    elif key == pyglet.window.key.UP:
        #player.y += 16
        game.player.walk(0, 1)
    elif key == pyglet.window.key.DOWN:
        #player.y -= 16
        game.player.walk(0, -1)
    engine.signals.handle_signals()

pyglet.app.run()
