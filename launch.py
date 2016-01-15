#!/usr/bin/env python3

import interfaces.pyglet

from engine import *

game = game.Game()

pikachu = beast.BeastFamily()
pikachu.name = 'Pikachu'
pikachu.type = 'Electrik'

pikagroup = zone.WildGroup(pikachu, 10) # group of 10 pikachus
pikazone = zone.Zone('grass')
pikazone.groups = [pikagroup]


bourg = map.Map(5, 5)
bourg.zones = [pikazone]
bourg.tiles = (
    (
        (tile.Grass(), tile.Grass(), tile.HighGrass(pikazone), tile.Grass(), tile.Grass()),
        (tile.Grass(), tile.HighGrass(pikazone), tile.HighGrass(pikazone), tile.HighGrass(pikazone), tile.Grass()),
        (tile.Grass(), tile.HighGrass(pikazone), tile.HighGrass(pikazone), tile.HighGrass(pikazone), tile.Grass()),
        (tile.Grass(), tile.HighGrass(pikazone), tile.HighGrass(pikazone), tile.HighGrass(pikazone), tile.Grass()),
        (tile.Grass(), tile.Grass(), tile.Grass(), tile.Grass(), tile.Grass()),
    ),
) # event tiles are automatically put in bourg.events
for z, level in enumerate(bourg.tiles):
    for y, line in enumerate(level):
        for x, tile in enumerate(line):
            tile.x, tile.y, tile.z = x, y, z
bourg.events += [character.Character(), character.Trainer(), object.Object()]
bourg.levels = len(bourg.tiles)
game.maps.append(bourg)

player = player.Player()
player.map = bourg
player.position = (0, 0)
player.beastiary = beast.Beastiary()
game.player = player

signals.reg_signal('moved', lambda _, char, map, old, new: map.moved(char, old, new))

if __name__ == '__main__':
    game.run()
