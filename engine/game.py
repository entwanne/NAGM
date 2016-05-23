from .gobject import GObject
from . import signals, event
from . import meta
import time

@meta.apply
class Game(GObject):
    'Main class for the game, contains maps, players and events'

    __attributes__ = ('maps', 'players', 'events')

    def __init__(self, **kwargs):
        kwargs.setdefault('maps', {})
        kwargs.setdefault('players', [])
        kwargs.setdefault('events', [])
        super().__init__(**kwargs)

    def run(self):
        'Run game forever'
        while True:
            self.handle_signals()
            self.step()
            time.sleep(0.3)

    def handle_signals(self):
        'Wrapper to signals.handle_signals'
        signals.handle_signals(self)

    @staticmethod
    def have_signals():
        'Wrapper to signals.have_signals'
        return signals.have_signals()

    @property
    def events(self):
        'Wrapper to event.events'
        return event.events

    @events.setter
    def events(self, value):
        'Reset event.events'
        event.events = value

    def step(self):
        'Game-loop iteration'
        # step active maps and events on these maps
        maps = set(player.map for player in self.players)
        events = set(event for event in self.events if event.map is None or event.map in maps)
        for obj in maps | events:
            if hasattr(obj, 'step'):
                obj.step(self)

    def save(self, filename):
        'Dump game-state to a file'
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename):
        'Load game from a dump file'
        import pickle
        with open(filename, 'rb') as f:
            game = pickle.load(f)
        if not isinstance(game, cls):
            raise TypeError('Wrong game type')
        return game
