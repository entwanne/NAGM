#!/usr/bin/env python3

DEBUG = True
INTERFACE = 'interfaces.pyglet'
GAME = 'games.test_game'


from importlib import import_module

import_module(INTERFACE)
import engine
engine.load_modules()

game_mod = import_module(GAME)

import os.path

if os.path.exists('game.save'):
    game = engine.game.Game.load('game.save')
else:
    game = game_mod.init_game()


if __name__ == '__main__':
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
