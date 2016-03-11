import engine
from .zones import zone

#Edge = engine.tile.over(engine.tile.Grass, engine.tile.Edge)
Water = engine.tile.over(engine.tile.Grass, engine.tile.Water)

def stairs_directions(y):
    return {(x, y): (x, 0, y) for x in (-1, 0, 1)}

tile_chars = {
    '.': engine.tile.Grass,
    '*': lambda: engine.tile.HighGrass.spawn(zone=zone),
    '|': engine.tile.Tree,
    'x': engine.tile.Rock,
    '=': lambda: engine.tile.Stairs(directions=stairs_directions(1)),
    '#': lambda: engine.tile.Stairs(directions=stairs_directions(-1)),
    #'-': Edge,
    '>': lambda: engine.tile.Teleport(pos=(4,0), map_name='road'),
    '<': lambda: engine.tile.Teleport(pos=(3,17), map_name='bourg'),
    '~': Water,
    ' ': engine.tile.Hole,
}

def make_tiles(str_tiles):
    return [
        [
            [tile_chars.get(t, engine.tile.Tile)() for t in line]
            for line in reversed(level.splitlines()) if line
        ]
        for level in str_tiles
    ]
