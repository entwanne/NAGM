#!/usr/bin/env python3

DEBUG = True

import interfaces.pyglet

import game_defs

import os.path

if os.path.exists('game.save'):
    game = None
    import engine
    import pickle
    with open('game.save', 'rb') as f:
        game_id, defs = pickle.load(f)
    print(game_id)
    objects = {}
    def load(obj):
        if isinstance(obj, tuple):
            return tuple(load(v) for v in obj)
        if isinstance(obj, list):
            return [load(v) for v in obj]
        if isinstance(obj, dict):
            return {load(k): load(v) for (k, v) in obj.items()}
        if obj in objects:
            return objects[obj]
        return obj
    for objid, clsname, attrs in defs:
        cls = engine.meta.created[clsname]
        attrs = {k: load(v) for (k, v) in attrs.items()}
        objects[objid] = cls(**attrs)
    game = objects[game_id]
    objects = []
else:
    game = game_defs.init_game()


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
