#!/usr/bin/env python3

import interfaces.pyglet

from engine import *

game = game.Game()

pikachu = beast.BeastFamily('Pikachu', 'Electrik')
carapuce = beast.BeastFamily('Carapuce', 'Eau')

pikagroup = zone.WildGroup(pikachu, 10) # group of 10 pikachus
caragroup = zone.WildGroup(carapuce, 4) # group of 4 carapuces
zone = zone.Zone('grass', [pikagroup, caragroup])

tile_chars = {
    '.': tile.Grass,
    '*': lambda: tile.HighGrass(zone),
    '|': tile.Tree,
    '>': lambda: tile.Teleport((4,0), 'road'),
    '<': lambda: tile.Teleport((3,17), 'bourg'),
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
bourg_char = character.Character((0,17,0))
bourg_char.actioned = lambda game, player: print('Hello')
bourg.add_event(bourg_char)
#bourg.add_event(object.Object())
game.maps['bourg'] = bourg

road_tiles = []
road_tiles.append("""
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


player = player.Player((0, 2, 0), bourg)
player.beastiary = beast.Beastiary()
game.player = player

if __name__ == '__main__':
    game.run()
