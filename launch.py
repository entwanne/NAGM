#!/usr/bin/env python3

DEBUG = True

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
    'x': tile.Rock,
    '=': lambda: tile.Stairs({(0, 1): (0, 0, 1)}),
    '#': lambda: tile.Stairs({(0, -1): (0, 0, -1)}),
    '-': tile.Hole,
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


bourg_char = character.Character((1,16,0), bourg)
def bourg_char_actioned(game, player, map, pos):
    print('Hello')
    x, y, z = pos
    dx, dy = player.x - x, player.y - y
    bourg_char.turn(dx, dy)
bourg_char.actioned = bourg_char_actioned
def bourg_char_step(game):
    bourg_char.n = (bourg_char.n + 1) % 5
    if bourg_char.n:
        return
    pos = bourg_char.position
    bourg_char.walk()
    if pos == bourg_char.position:
        dx, dy = bourg_char.direction
        dc = dx + dy * 1j
        dc *= 1j
        dx, dy = int(dc.real), int(dc.imag)
        bourg_char.turn(dx, dy)
bourg_char.n = 0
bourg_char.step = bourg_char_step
event.events.append(bourg_char)
#event.events.append(object.Object())


player = player.Player((0, 2, 0), bourg)
player.beastiary = beast.Beastiary()
game.player = player
game.events = event.events
game.events.append(player)


if __name__ == '__main__':
    if DEBUG:
        import code, threading, signal
        class MainThread(threading.Thread):
            def run(self):
                game.run()
                signal.alarm(1)
        def handler(*_):
            raise EOFError
        signal.signal(signal.SIGALRM, handler)
        MainThread(daemon=True).start()
        code.interact(local={'game': game})
    else:
        game.run()
