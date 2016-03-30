DEBUG = True
INTERFACE = 'nagm.interfaces.pyglet'
GAME = 'nagm.games.test_game'

from importlib import import_module

game_mod = import_module(GAME)
import_module(INTERFACE)
from . import engine
engine.load_modules()

import os.path

if os.path.exists('game.save'):
    game = engine.game.Game.load('game.save')
    # + error if modules from game are loaded (except game.defs) ?
else:
    game = game_mod.init_game()

if DEBUG:
    import code, threading, signal
    main_thread_id = threading.get_ident()
    class GameThread(threading.Thread):
        def run(self):
            game.run()
            signal.pthread_kill(main_thread_id, signal.SIGQUIT)
    GameThread(daemon=True).start()
    code.interact(local={'game': game, 'engine': engine})
else:
    game.run()
