from .gobject import GObject
from . import meta

@meta.apply
class Type(GObject):
    __attributes__ = ('name', 'relations')

    def __init__(self, **kwargs):
        kwargs.setdefault('relations', {})
        super().__init__(**kwargs)

    # Move relations handler in games.test_game ?
    def set_over(self, rtype, mul):
        self.relations[rtype] = mul

    def over(self, rtype):
        return self.relations.get(rtype, 1)
