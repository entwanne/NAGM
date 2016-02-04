from .gobject import GObject
from . import meta

@meta.apply
class Attack(GObject):
    __attributes__ = ('name', 'damages',)

    def use(self, sender, receiver):
        receiver.damages(self.damages * sender.att / receiver.dfse)

lutte = Attack(name='lutte', damages=10)
