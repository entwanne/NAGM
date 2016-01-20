from .gobject import GObject
from . import signals
import time

class Game(GObject):
    def __init__(self):
        self.maps = {}
        self.player = None

    def run(self):
        while True:
            self.handle_signals()
            time.sleep(0.3)

    def handle_signals(self):
        signals.handle_signals(self)

    @staticmethod
    def reg_signal(*args):
        signals.reg_signal(*args)

    @staticmethod
    def have_signals():
        return signals.have_signals()
