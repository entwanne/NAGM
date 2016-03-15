from nagm import engine

import nagm.engine.resources
import os.path
engine.resources.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'res')))

def init_game():
    from . import defs

    game = engine.game.Game()

    from .maps import bourg
    from .maps import road
    game.maps['bourg'] = bourg
    game.maps['road'] = road

    char1 = defs.BourgChar(
        position=(1,16,0),
        map=bourg,
        dialogs=(
            'Hello',
            'World',
            '!'
        ),
    )
    game.events.append(char1)
    char2 = defs.BourgChar(
        position=(9,0,0),
        map=road,
        dialogs=(
            'Hug',
        ),
    )
    game.events.append(char2)
    #event.events.append(object.Object())

    from .beasts import carapuce, pikachu
    defs.add_player(game, 'Red', bourg, (0, 2, 0), carapuce, pikachu)
    defs.add_player(game, 'Blue', bourg, (0, 2, 0), pikachu)

    spawner = defs.ActionEvent(
        position=(0, 1, 0),
        map=bourg,
        action_callback=engine.bind.cb(
            defs.add_player, game, 'Green', bourg, (0, 2, 0), pikachu
        )
    )
    game.events.append(spawner)

    group = engine.dialog.DialogGroupSpawner()
    timer = engine.event.Timer(
        clock=engine.clock.Clock(2),
        signal=engine.bind.cb(
            game.events.append,
            engine.bind._(
                defs.BourgChar,
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
