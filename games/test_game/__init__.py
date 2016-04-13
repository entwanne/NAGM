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

    defs.BourgChar.spawn(
        position=(1,16,0),
        map=bourg,
        dialogs=(
            'Hello',
            'World',
            '!'
        ),
    )
    defs.BourgChar.spawn(
        position=(9,0,0),
        map=road,
        dialogs=(
            'Hug',
        ),
    )

    from .beasts import carapuce, pikachu
    defs.add_player(game, 'Red', bourg, (0, 2, 0), carapuce, pikachu)
    defs.add_player(game, 'Blue', bourg, (0, 2, 0), pikachu)

    defs.ActionEvent.spawn(
        position=(0, 1, 0),
        map=bourg,
        action_callback=engine.bind.cb(
            defs.add_player, game, 'Green', bourg, (0, 2, 0), pikachu
        )
    )

    group = engine.dialog.DialogGroupSpawner()
    engine.event.Timer.spawn(
        clock=engine.clock.Clock(2),
        signal=engine.bind.cb(
            defs.BourgChar.spawn,
            position=(5,3,0),
            map=bourg,
            dialog_group=group,
            dialogs=(
                'Bonjour, tu aimes les frites ?',
                ('oui', group.callback('cool'), 'non', None),
            )
        )
    )

    return game
