from ..gobject import GObject
from ..signals import sighandler

class ActionEventCallback(GObject):
    'An event that calls a signal when it is actioned'

    __attributes__ = ('action_callback',)

    @sighandler
    def actioned(self, *args):
        self.action_callback(*args)

class CrossEventCallback(GObject):
    'An event that calls a signal when it is crossed'

    __attributes__ = ('cross_callback',)

    @sighandler
    def crossed(self, *args):
        self.cross_callback(*args)
