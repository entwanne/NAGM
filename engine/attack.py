from .gobject import GObject
from . import meta

@meta.apply
class Attack(GObject):
    __attributes__ = ('name', 'type', 'damages',)

    def use(self, sender, receiver):
        dam = self.damages * sender.att / receiver.dfse
        dam *= self.type.over(receiver.type)
        receiver.damages(dam)
