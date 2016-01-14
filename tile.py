class Tile:
    pass

class Empty(Tile): pass

class Grass(Tile): pass

class Rock(Tile): pass

tiles = {
    ' ': Empty,
    '.': Grass,
    'x': Rock,
}
