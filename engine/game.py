from .gobject import GObject
from . import signals, event
from . import meta
import time

@meta.apply
class Game(GObject):
    __attributes__ = ('maps', 'player', 'events')

    def __init__(self, **kwargs):
        kwargs.setdefault('maps', {})
        kwargs.setdefault('player', None)
        kwargs.setdefault('events', [])
        super().__init__(**kwargs)

    def run(self):
        while True:
            self.handle_signals()
            self.step_events()
            time.sleep(0.3)

    def handle_signals(self):
        signals.handle_signals(self)

    @staticmethod
    def have_signals():
        return signals.have_signals()

    @property
    def events(self):
        return event.events

    @events.setter
    def events(self, value):
        event.events = value

    def step(self):
        if self.player.battle:
            self.player.battle.step(self)
        for event in self.events:
            if (event.map is None or event.map == self.player.map) and hasattr(event, 'step'):
                event.step(self)

    def save(self, filename):
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename):
        import pickle
        with open(filename, 'rb') as f:
            game = pickle.load(f)
        if not isinstance(game, cls):
            raise TypeError('Wrong game type')
        return game
