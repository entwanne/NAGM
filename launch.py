#!/usr/bin/env python3

DEBUG = True

import interfaces.pyglet

from engine import *

class BourgChar(character.Character):
    def __init__(self, *args, **kwargs):
        character.Character.__init__(self, *args, **kwargs)
        self.n = 0

    def actioned(self, game, player, map, pos):
        x, y, z = pos
        dx, dy = player.x - x, player.y - y
        self.turn(dx, dy)
        dialog.Dialog('Hello', player, self)

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


game = game.Game()


pikachu = beast.BeastFamily('Pikachu', 'Electrik')
carapuce = beast.BeastFamily('Carapuce', 'Eau')

pikagroup = zone.WildGroup(pikachu, 5) # group of 10 pikachus
caragroup = zone.WildGroup(carapuce, 2) # group of 4 carapuces
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


event.events.append(BourgChar((1,16,0), bourg))
#event.events.append(object.Object())


player = player.Player((0, 2, 0), bourg)
player.beastiary = beast.Beastiary()
player.beast = beast.Beast(carapuce)
game.player = player
game.events = event.events
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
