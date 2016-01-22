from .gobject import GObject

class Dialog(GObject):
    __attributes__ = GObject.__attributes__ + ('msg', 'dest', 'src')

    def __init__(self, msg, dest, src=None):
        print(msg)
        self.msg, self.dest, self.src = msg, dest, src
        dest.dialog = self
        if src is not None:
            src.dialog = self

    def action(self, game, player):
        self.dest.dialog = None
        if self.src is not None:
            self.src.dialog = None
