from .gobject import GObject

class Dialog(GObject):
    __attributes__ = GObject.__attributes__ + ('msg', 'dest', 'src')

    def __init__(self, **kwargs):
        kwargs['msg']
        kwargs['dest']
        kwargs.setdefault('src', None)
        GObject.__init__(self, **kwargs)
        print(self.msg)
        self.dest.dialog = self
        if self.src is not None:
            self.src.dialog = self

    def action(self, game, player):
        self.dest.dialog = None
        if self.src is not None:
            self.src.dialog = None
