import engine
from .zones import zone

Edge = engine.tile.over(engine.tile.Grass, engine.tile.Edge)
Water = engine.tile.over(engine.tile.Grass, engine.tile.Water)

tile_chars = {
    '.': engine.tile.Grass,
    '*': lambda: engine.tile.HighGrass(zone=zone),
    '|': engine.tile.Tree,
    'x': engine.tile.Rock,
    '=': lambda: engine.tile.Stairs(directions={(0, 1): (0, 0, 1)}),
    '#': lambda: engine.tile.Stairs(directions={(0, -1): (0, 0, -1)}),
    '-': Edge,
    '>': lambda: engine.tile.Teleport(pos=(4,0), map_name='road'),
    '<': lambda: engine.tile.Teleport(pos=(3,17), map_name='bourg'),
    '~': Water,
}

def make_tiles(str_tiles):
    return [
        [
            [tile_chars.get(t, engine.tile.Tile)() for t in line]
            for line in reversed(level.splitlines()) if line
        ]
        for level in str_tiles
    ]
