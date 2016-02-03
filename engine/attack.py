from .gobject import GObject
from . import meta

@meta.apply
class Attack(GObject):
    __attributes__ = ('name', 'att',)

    def use(self, sender, receiver):
        receiver.hp -= self.att

lutte = Attack(name='lutte', att=10)
