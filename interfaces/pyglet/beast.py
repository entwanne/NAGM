import pyglet
import nagm.engine.resources as res

from collections import defaultdict

textures = defaultdict(
    lambda: pyglet.image.Texture.create(16, 16),
    {
        'Pikachu': pyglet.image.load(res.get('025.png')),
        'Carapuce': pyglet.image.load(res.get('007.png')),
    }
)
