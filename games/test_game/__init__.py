import engine

from .defs import *

def init_game():
    game = engine.game.Game()

    from .maps import bourg
    from .maps import road
    game.maps['bourg'] = bourg
    game.maps['road'] = road

    char1 = BourgChar(
        position=(1,16,0),
        map=bourg,
        dialogs=(
            'Hello',
            'World',
            '!'
        ),
    )
    game.events.append(char1)
    #event.events.append(object.Object())

    player = engine.player.Player(name='Red', position=(0, 2, 0), map=bourg)
    player.beastiary = engine.beast.Beastiary()
    from .beasts import carapuce
    player.beast = engine.beast.Beast(family=carapuce, dfse=10)
    game.players.append(player)
    game.events.append(player)

    player = engine.player.Player(name='Blue', position=(0, 2, 0), map=bourg)
    player.beastiary = engine.beast.Beastiary()
    from .beasts import pikachu
    player.beast = engine.beast.Beast(family=pikachu, dfse=10)
    game.players.append(player)
    game.events.append(player)

    group = engine.dialog.DialogGroupSpawner()
    timer = engine.event.Timer(
        clock=engine.clock.Clock(2),
        signal=engine.bind.cb(
            game.events.append,
            engine.bind._(
                BourgChar,
                position=(5,3,0),
                map=bourg,
                dialog_group=group,
                dialogs=(
                    'Bonjour, tu aimes les frites ?',
                    ('oui', group.callback('cool'), 'non', None),
                )
            )
        )
    )
    game.events.append(timer)

    return game
