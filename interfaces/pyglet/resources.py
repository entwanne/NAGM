import pyglet
import nagm.engine.resources as res

grounds_img = pyglet.image.load(res.get('sols.png'))
grounds_imggrid = pyglet.image.ImageGrid(grounds_img, 50, 12)
grounds_texgrid = pyglet.image.TextureGrid(grounds_imggrid)
trees_img = pyglet.image.load(res.get('arbres.png'))
trees_imggrid = pyglet.image.ImageGrid(trees_img, 50, 12)
trees_texgrid = pyglet.image.TextureGrid(trees_imggrid)
players_img = pyglet.image.load(res.get('persos.png'))
players_imggrid = pyglet.image.ImageGrid(players_img, 2, 12)
players_texgrid = pyglet.image.TextureGrid(players_imggrid)

def get_empty_tile():
    return pyglet.image.Texture.create(16, 16)
