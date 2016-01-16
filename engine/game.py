from .gobject import GObject
from . import signals

class Game(GObject):
    def __init__(self):
        self.maps = {}
        self.player = None

    def run(self):
        pass

    @staticmethod
    def handle_signals():
        signals.handle_signals()

    @staticmethod
    def reg_signal(*args):
        signals.reg_signal(*args)

    @staticmethod
    def have_signals():
        return signals.have_signals()
