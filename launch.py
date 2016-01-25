#!/usr/bin/env python3

DEBUG = True

import interfaces.pyglet
import engine
engine.load_modules()

import test_game

import os.path

if os.path.exists('game.save'):
    import pickle
    with open('game.save', 'rb') as f:
        game = pickle.load(f)
    print(game.events)
else:
    game = test_game.init_game()


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
