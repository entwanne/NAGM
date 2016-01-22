#!/usr/bin/env python3

DEBUG = True

import interfaces.pyglet

from engine import *
from game_defs import BourgChar

game = game.Game()


pikachu = beast.BeastFamily(name='Pikachu', type='Electrik')
carapuce = beast.BeastFamily(name='Carapuce', type='Eau')

pikagroup = zone.WildGroup(family=pikachu, population=5) # group of 10 pikachus
caragroup = zone.WildGroup(family=carapuce, population=2) # group of 4 carapuces
zone = zone.Zone(type='grass', groups=[pikagroup, caragroup])


tile_chars = {
    '.': tile.Grass,
    '*': lambda: tile.HighGrass(zone=zone),
    '|': tile.Tree,
    'x': tile.Rock,
    '=': lambda: tile.Stairs(directions={(0, 1): (0, 0, 1)}),
    '#': lambda: tile.Stairs(directions={(0, -1): (0, 0, -1)}),
    '-': tile.Hole,
    '>': lambda: tile.Teleport(pos=(4,0), map_name='road'),
    '<': lambda: tile.Teleport(pos=(3,17), map_name='bourg'),
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
        [tile_chars.get(t, tile.Tile)() for t in line]
        for line in reversed(level.splitlines()) if line
    ]
    for level in bourg_tiles
]
bourg_zones = [zone]
bourg = map.Map.from_tiles(bourg_tiles, bourg_zones)
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
        [tile_chars.get(t, tile.Tile)() for t in line]
        for line in reversed(level.splitlines()) if line
    ]
    for level in road_tiles
]
road_zones = [zone]
road = map.Map.from_tiles(road_tiles, road_zones)
game.maps['road'] = road

game.events.append(BourgChar(position=(1,16,0), map=bourg))
#event.events.append(object.Object())


player = player.Player(position=(0, 2, 0), map=bourg)
player.beastiary = beast.Beastiary()
player.beast = beast.Beast(family=carapuce)
game.player = player
game.events.append(player)


if __name__ == '__main__':
    if DEBUG:
        import code, threading, signal
        main_thread_id = threading.get_ident()
        class GameThread(threading.Thread):
            def run(self):
                game.run()
                signal.pthread_kill(main_thread_id, signal.SIGQUIT)
        GameThread(daemon=True).start()
        import engine
        code.interact(local={'game': game, 'engine': engine})
    else:
        game.run()
