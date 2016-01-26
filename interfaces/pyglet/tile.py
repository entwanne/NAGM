import engine.meta

from .resources import grounds_texgrid, trees_texgrid

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
