from ..gobject import GObject
from ..signals import sighandler

class ActionEventCallback(GObject):
    __attributes__ = ('action_callback',)

    @sighandler
    def actioned(self, *args):
        self.action_callback(*args)

class CrossEventCallback(GObject):
    __attributes__ = ('cross_callback',)

    @sighandler
    def crossed(self, *args):
        self.cross_callback(*args)
