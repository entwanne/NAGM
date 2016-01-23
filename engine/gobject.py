from .meta import GObjectMeta
from . import signals
from . import meta

@meta.apply
class GObject(metaclass=GObjectMeta):
    # Attributes of the object (owned by this object)
    __attributes__ = ('id',)
    # Other objects linked to this one
    __dependencies__ = ()

    def __init__(self, **kwargs):
        kwargs.setdefault('id', '<{}>'.format(id(self)))
        for key in self.__attributes__:
            setattr(self, key, kwargs.pop(key))
        if kwargs:
            raise TypeError('Unexpected attributes {}'.format(', '.join(kwargs.keys())))

    def send(self, handler, *args, **kwargs):
        signals.send_signal(handler, self, *args, **kwargs)

    def dump(self, deps=None, seen=None):
        if deps is None:
            deps = []
        if seen is None:
            seen = []
        seen.append(self)
        dic = {}
        for key in self.__attributes__:
            dic[key] = dump(getattr(self, key), deps, seen)
        deps.append((self.id, type(self).__fullname__, dic))
        for key in self.__dependencies__:
            dump(getattr(self, key), deps, seen)
        return deps

    def __getstate__(self):
        return {k: getattr(self, k) for k in self.__attributes__}

def dump(obj, deps, seen):
    if isinstance(obj, GObject):
        if obj not in seen:
            obj.dump(deps, seen)
        return obj.id
    if isinstance(obj, tuple):
        return tuple(dump(v, deps, seen) for v in obj)
    if isinstance(obj, list):
        return [dump(v, deps, seen) for v in obj]
    if isinstance(obj, dict):
        return {dump(k, deps, seen): dump(v, deps, seen) for (k, v) in obj.items()}
    if obj is None or isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float):
        return obj
    raise TypeError('Cannot dump object of type {}'.format(repr(type(obj))))
