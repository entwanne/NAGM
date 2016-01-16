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
    '>': lambda: tile.Teleport((0,0), 'road'),
    '<': lambda: tile.Teleport((3,16), 'bourg'),
}

bourg_tiles = []
bourg_tiles.append("""
...>......
..........
..........
..........
..........
..........
..........
..........
..........
....***...
....***>..
....***...
.....*....
..........
..........
..........
..........
""")
bourg_tiles = [
    [
        [tile_chars.get(t, tile.Tile)() for t in line]
        for line in reversed(level.splitlines()) if line
    ]
    for level in bourg_tiles
]
bourg_events = (character.Character(), character.Trainer(), object.Object())
bourg_zones = [zone]
bourg = map.Map.from_tiles(bourg_tiles, bourg_events, bourg_zones)
game.maps['bourg'] = bourg

road_tiles = []
road_tiles.append("""
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
..**..
<.....
""")
road_tiles = [
    [
        [tile_chars.get(t, tile.Tile)() for t in line]
        for line in reversed(level.splitlines()) if line
    ]
    for level in road_tiles
]
road_events = ()
road_zones = [zone]
road = map.Map.from_tiles(road_tiles, road_events, road_zones)
game.maps['road'] = road


player = player.Player()
player.map = bourg
player.position = (0, 0)
player.beastiary = beast.Beastiary()
game.player = player

if __name__ == '__main__':
    game.run()
