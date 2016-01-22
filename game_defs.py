import engine
import engine.game
import engine.character
import engine.map
import engine.tile
import engine.zone
import engine.beast
import engine.dialog

class BourgChar(engine.character.Character):
    def __init__(self, **kwargs):
        engine.character.Character.__init__(self, **kwargs)
        self.n = 0

    def actioned(self, game, player, map, pos):
        x, y, z = pos
        dx, dy = player.x - x, player.y - y
        self.turn(dx, dy)
        engine.dialog.Dialog(msg='Hello', dest=player, src=self)

    def step(self, game):
        self.n = (self.n + 1) % 5
        if self.n:
            return
        if not self.walk():
            dx, dy = self.direction
            dc = dx + dy * 1j
            dc *= 1j
            dx, dy = int(dc.real), int(dc.imag)
            self.turn(dx, dy)

def init_game():
    game = engine.game.Game()


    pikachu = engine.beast.BeastFamily(name='Pikachu', type='Electrik')
    carapuce = engine.beast.BeastFamily(name='Carapuce', type='Eau')

    pikagroup = engine.zone.WildGroup(family=pikachu, population=5) # group of 10 pikachus
    caragroup = engine.zone.WildGroup(family=carapuce, population=2) # group of 4 carapuces
    zone = engine.zone.Zone(type='grass', groups=[pikagroup, caragroup])


    tile_chars = {
        '.': engine.tile.Grass,
        '*': lambda: engine.tile.HighGrass(zone=zone),
        '|': engine.tile.Tree,
        'x': engine.tile.Rock,
        '=': lambda: engine.tile.Stairs(directions={(0, 1): (0, 0, 1)}),
        '#': lambda: engine.tile.Stairs(directions={(0, -1): (0, 0, -1)}),
        '-': engine.tile.Hole,
        '>': lambda: engine.tile.Teleport(pos=(4,0), map_name='road'),
        '<': lambda: engine.tile.Teleport(pos=(3,17), map_name='bourg'),
    }

    bourg_tiles = []
    bourg_tiles.append("""
...>......||||
..........||||
..........||||
..........||||
..........||||
..........||||
..........||||
..........||||
....***...||||
....***>..||||
....***...||||
.....*....||||
..........||||
..........||||
..........||||
..........||||
||||||||||||||
||||||||||||||
""")
    bourg_tiles.append("""
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
          ||||
||||||||||||||
||||||||||||||
""")
    bourg_tiles = [
        [
            [tile_chars.get(t, engine.tile.Tile)() for t in line]
            for line in reversed(level.splitlines()) if line
        ]
        for level in bourg_tiles
    ]
    bourg_zones = [zone]
    bourg = engine.map.Map.from_tiles(bourg_tiles, bourg_zones)
    game.maps['bourg'] = bourg

    road_tiles = []
    road_tiles.append("""
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||x=xxxx||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||<.....||||
""")
    road_tiles.append("""
||||......||||
||||......||||
||||......||||
||||......||||
||||......||||
||||......||||
||||......||||
||||......||||
||||.#....||||
||||- ----||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
""")
    road_tiles = [
        [
            [tile_chars.get(t, engine.tile.Tile)() for t in line]
            for line in reversed(level.splitlines()) if line
        ]
        for level in road_tiles
    ]
    road_zones = [zone]
    road = engine.map.Map.from_tiles(road_tiles, road_zones)
    game.maps['road'] = road

    game.events.append(BourgChar(position=(1,16,0), map=bourg))
    #event.events.append(object.Object())


    player = engine.player.Player(position=(0, 2, 0), map=bourg)
    player.beastiary = engine.beast.Beastiary()
    player.beast = engine.beast.Beast(family=carapuce)
    game.player = player
    game.events.append(player)

    return game
