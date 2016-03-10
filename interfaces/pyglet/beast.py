import pyglet

from collections import defaultdict

textures = defaultdict(
    lambda: pyglet.image.Texture.create(16, 16),
    {
        'Pikachu': pyglet.image.load('res/025.png'),
        'Carapuce': pyglet.image.load('res/007.png'),
    }
)
