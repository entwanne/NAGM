import engine.meta

from .resources import grounds_texgrid, trees_texgrid

@engine.meta.register('engine.tile.Tile')
class _:
    img = grounds_texgrid[0, 0]
    def refresh(self, map, pos): pass

@engine.meta.register('engine.tile.Grass')
@engine.meta.register('engine.tile.Edge')
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

@engine.meta.register('engine.tile.Water')
class Water:
    imgs = {
        # left, right, down, up
        # True = not water
        (True, False, True, False): grounds_texgrid[41, 3],
        (True, False, False, True): grounds_texgrid[43, 3],
        (False, True, True, False): grounds_texgrid[41, 5],
        (False, True, False, True): grounds_texgrid[43, 5],
        (True, False, False, False): grounds_texgrid[42, 3],
        (False, True, False, False): grounds_texgrid[42, 5],
        (False, False, True, False): grounds_texgrid[41, 4],
        (False, False, False, True): grounds_texgrid[43, 4],
    }
    img = grounds_texgrid[42, 4]
    def refresh(self, map, pos):
        x, y, z = pos
        nexts = tuple(not isinstance(map.get_tile((x + dx, y + dy, z)), Water)
                      for (dx, dy) in zip((-1, 1, 0, 0), (0, 0, -1, 1)))
        if nexts in self.imgs:
            self.img = self.imgs[nexts]
