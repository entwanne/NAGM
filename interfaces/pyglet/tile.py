import engine.meta

from .resources import grounds_texgrid, trees_texgrid, get_empty_tile

@engine.meta.register('engine.tile.Tile')
class _:
    img = None
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
class _:
    __Y, __X = 47, 0
    __left = True
    __trunk = True
    def refresh(self, map, pos):
        x, y, z = pos
        xtile = map.get_tile((x - 1, y, z))
        if isinstance(xtile, engine.tile.Tree) and xtile.__left:
            self.__left = False
            self.__X += 1
        ytile = map.get_tile((x, y - 1, z))
        if isinstance(ytile, engine.tile.Tree) and ytile.__trunk:
            self.__trunk = False
            self.__Y += 1
        ztile = map.get_tile((x, y, z - 1))
        if isinstance(ztile, engine.tile.Tree):
            if self.__trunk:
                self.__X, self.__Y = 0, 0
            else:
                self.__Y += 1

    @property
    def img(self):
        return trees_texgrid[self.__Y, self.__X]

@engine.meta.register('engine.tile.Rock')
class _:
    img = grounds_texgrid[32, 1]

@engine.meta.register('engine.tile.Stairs')
class _:
    img = grounds_texgrid[49, 0]
    def refresh(self, map, pos):
        x, y, z = pos
        if (0, 1) in self.directions:
            self.img = grounds_texgrid[49, 7]

@engine.meta.register('engine.tile.Water')
class _:
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
        nexts = tuple(not isinstance(map.get_tile((x + dx, y + dy, z)), engine.tile.Water)
                      for (dx, dy) in zip((-1, 1, 0, 0), (0, 0, -1, 1)))
        if nexts in self.imgs:
            self.img = self.imgs[nexts]

@engine.meta.register('engine.tile.Over')
class _:
    def refresh(self, map, pos):
        for tile in self.tiles:
            tile.refresh(map, pos)
            if tile.img is not None:
                self.img = tile.img
