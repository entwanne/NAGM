#!/usr/bin/env python3

"""
Gestion des niveaux (levels)

Un niveau correspond à un calque de tiles
Pour deux niveaux a et b avec a > b, a sera affiché au-dessus de b
Le niveau le plus bas est 0
Les éveènements sont toujours affichés au-dessus des niveaux auxquels ils appartiennent
Une différence de 1 niveau correspond à la taille du joueur (le joueur est cependant affiché sur 2 niveaux de tiles : la tête est affichée sur le niveau supérieur)
Il existe aussi des demi-niveaux : si le joueur est placé au niveau 0, il ne peut pas se déplacer sur une case niveau 0.5 (sauf case spéciale), mais l'inverse est vrai (comme le saut d'une bordure)

Les tiles sont toujours affichés en 2D avec un décalage en ordonnées conditionné par l'arrondi supérieur de son niveau
Par exemple, un arbre en (5,4,0) sera affiché en (5,4), mais ses feuilles en (5,4,1) seront affichées sur le tile (5,5) (il suffira de décaler de 1 le batch)
Une bordure en (3,2,0.5) sera affichée en (3,3), ce qui explique qu'en arrivant sur cette case, le joueur se trouve "téléporté" en (3,2,0) (descente d'un demi-niveau), soit (3,2), soit une case en-dessous sur l'affichage 2D.

-> les demi-niveaux doivent-ils réellement être décalés ? doivent-ils réellement exister (peuvent être remplacés par des niveaux simples avec propriétés spéciales) ? ou décalage de moitié ?
+ penser aux bordures à franchir latéralement (gauche<->droite) : si un perso est en (3,2,0.5) et se déplace vers la gauche (qui est du niveau en-dessous, avec bordure), il se retrouve en (3,2,0): en coords 2D, cela donne (3,2.5) -> (2,2), alors que dans Pokémon, c'est plutôt (3,2) -> (1,2)
"""

import pyglet

window = pyglet.window.Window(width=800, height=600)

batch = pyglet.graphics.Batch()
bggroup = pyglet.graphics.OrderedGroup(0)
fggroup = pyglet.graphics.OrderedGroup(1)

red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
blue = (0, 0, 255, 255)
white = (255, 255, 255, 255)

#batch.add(4,
#          pyglet.gl.GL_QUADS,
#          bggroup,
#          ('v2i', (10, 10, 790, 10, 790, 590, 10, 590)),
#          ('c4B', blue + red + white + green)
#)

grounds_img = pyglet.image.load('res/sols.png')
grounds_imggrid = pyglet.image.ImageGrid(grounds_img, 50, 12)
grounds_texgrid = pyglet.image.TextureGrid(grounds_imggrid)
import tile
tile.Grass.img = grounds_texgrid[49, 0]
tile.Rock.img = grounds_texgrid[22, 11]
from map import map
sprites = []
for y, line in enumerate(reversed(map)):
    for x, tile in enumerate(line):
        if hasattr(tile, 'img'):
            sprites.append(
                pyglet.sprite.Sprite(tile.img,
                                     x=x*16, y=y*16,
                                     batch=batch, group=bggroup)
            )


players_img = pyglet.image.load('res/persos.png')
player_img = players_img.get_region(9 * 16, 0, 16, 32)
player = pyglet.sprite.Sprite(player_img, x=3*16, y=5*16, batch=batch, group=fggroup)

@window.event
def on_draw():
    dx = window.width // 2 - player.x
    dy = window.height // 2 - player.y
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
        player.x -= 16
    elif key == pyglet.window.key.RIGHT:
        player.x += 16
    elif key == pyglet.window.key.UP:
        player.y += 16
    elif key == pyglet.window.key.DOWN:
        player.y -= 16

pyglet.app.run()
