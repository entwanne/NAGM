from .gobject import GObject

class Game(GObject):
    def __init__(self):
        self.maps = {}
        self.player = None

    def run(self):
        pass
