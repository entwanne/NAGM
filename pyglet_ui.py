#!/usr/bin/env python3

import pyglet

import engine.meta

@engine.meta.register('engine.player.Player')
class _:
    def move(self, *args, **kwargs):
        super().move(*args, **kwargs)
        print(self)
        self.sprite.set_position(self.x*16, self.y*16)

grounds_img = pyglet.image.load('res/sols.png')
grounds_imggrid = pyglet.image.ImageGrid(grounds_img, 50, 12)
grounds_texgrid = pyglet.image.TextureGrid(grounds_imggrid)

@engine.meta.register('engine.tile.Grass')
class _:
    sprite = grounds_texgrid[49, 0]

@engine.meta.register('engine.tile.HighGrass')
class _:
    sprite = grounds_texgrid[22, 11]

import engine
from init_game import game

window = pyglet.window.Window(width=800, height=600)

batch = pyglet.graphics.Batch()
tile_groups = [pyglet.graphics.OrderedGroup(2 * i) for i in range(game.maps[0].levels)]
event_groups = [pyglet.graphics.OrderedGroup(2 * i + 1) for i in range(game.maps[0].levels)]

sprites = []
for z, level in enumerate(game.maps[0].tiles):
    for y, line in enumerate(reversed(level)):
        for x, tile in enumerate(line):
            if hasattr(tile, 'sprite'):
                sprites.append(
                    pyglet.sprite.Sprite(
                        tile.sprite,
                        x=x*16, y=(y+z)*16,
                        batch=batch, group=tile_groups[z])
                )


players_img = pyglet.image.load('res/persos.png')
player_img = players_img.get_region(9 * 16, 0, 16, 32)
game.player.sprite = pyglet.sprite.Sprite(player_img, x=game.player.x*16, y=game.player.y*16, batch=batch, group=event_groups[0])

@window.event
def on_draw():
    dx = window.width // 2 - game.player.sprite.x
    dy = window.height // 2 - game.player.sprite.y
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
        game.player.walk(-1, 0)
    elif key == pyglet.window.key.RIGHT:
        game.player.walk(1, 0)
    elif key == pyglet.window.key.UP:
        game.player.walk(0, 1)
    elif key == pyglet.window.key.DOWN:
        game.player.walk(0, -1)
    engine.signals.handle_signals()

pyglet.app.run()
