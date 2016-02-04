import engine

from .defs import *

def init_game():
    game = engine.game.Game()

    from .maps import bourg
    from .maps import road
    game.maps['bourg'] = bourg
    game.maps['road'] = road

    game.events.append(BourgChar(position=(1,16,0), map=bourg))
    #event.events.append(object.Object())

    player = engine.player.Player(position=(0, 2, 0), map=bourg)
    player.beastiary = engine.beast.Beastiary()
    from .beasts import carapuce
    player.beast = engine.beast.Beast(family=carapuce, dfse=10)
    game.player = player
    game.events.append(player)

    timer = engine.event.Timer(
        clock=engine.clock.Clock(2),
        signal=engine.bind.cb(
            game.events.append,
            engine.bind._(BourgChar2, position=(5,3,0), map=bourg)
        )
    )
    game.events.append(timer)

    return game
