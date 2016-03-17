from .gobject import GObject
from .meta import GObjectMeta

class StatsRefs:
    def __init__(self, cls, **kwargs):
        self.cls = cls
        self.values = kwargs

    def stats(self):
        return self.cls.from_values(**self.values)

class Stat(GObject):
    __attributes__ = ('value', 'default',)

    def __init__(self, **kwargs):
        kwargs.setdefault('default', kwargs['value'])
        super().__init__(**kwargs)

    @classmethod
    def from_value(cls, value, **kwargs):
        return cls(value=value, **kwargs)

    def set(self, value):
        self.value = value

    def reset(self):
        self.value = self.default

class MinMaxStat(Stat):
    __attributes__ = ('min', 'max',)

    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0)
        # if max is None, max is default
        kwargs.setdefault('max', None)
        super().__init__(**kwargs)

    def set(self, value):
        value = min(max(value, self.min), self.max)
        super().set(value)

    @property
    def max(self):
        if self._max is None:
            return self.default
        return self._max

    @max.setter
    def max(self, value):
        if hasattr(self, '_max') and self._max is None:
            self.default = value
        else:
            self._max = value

    def __getstate__(self):
        state = super().__getstate__()
        if self._max is None:
            del state['max']
        return state

class StatHelper:
    class Value(int):
        def __new__(cls, stat):
            return super().__new__(cls, stat.value)
        def __init__(self, stat):
            object.__setattr__(self, 'stat', stat)
        def __getattr__(self, name):
            return getattr(self.stat, name)
        def __setattr__(self, name, value):
            setattr(self.stat, name, value)

    def __init__(self, name, cls=Stat):
        self.attr = '_' + name
        self.cls = cls
        self.values_names = {'{}_{}'.format(name, attr): attr for attr in cls.__attributes__}
        self.values_names[name] = 'value'

    def _get(self, instance):
        return getattr(instance, self.attr)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.Value(self._get(instance))

    def __set__(self, instance, value):
        self._get(instance).set(value)

class StatsMeta(GObjectMeta):
    def __new__(cls, name, bases, dict):
        attributes = []
        helpers = {}
        for base in bases:
            if isinstance(base, cls):
                helpers.update(base.__stat_helpers__)
        for key, value in dict.items():
            if isinstance(value, StatHelper):
                helpers[key] = value
                attributes.append(value.attr)
        dict['__attributes__'] = dict.get('__attributes__', ()) + tuple(attributes)
        dict['__stat_helpers__'] = helpers
        return super().__new__(cls, name, bases, dict)

class BaseStats(GObject, metaclass=StatsMeta):
    @classmethod
    def from_values(cls, **kwargs):
        stats = {}
        for stat_helper in cls.__stat_helpers__.values():
            items = stat_helper.values_names.items() # [('hp', 'value'), ('hp_min', 'min'), ...]
            stat_kwargs = {attr: kwargs.pop(name) for name, attr in items if name in kwargs}
            if stat_kwargs:
                stats[stat_helper.attr] = stat_helper.cls(**stat_kwargs)
        #return cls(**stats, **kwargs)
        kwargs.update(stats)
        return cls(**kwargs)

    @property
    def values(self):
        "{'hp': 50, ...}"
        return {attr: getattr(self, attr) for attr in self.__stat_helpers__}

    def apply(self, stats):
        for key, diff in stats.items():
            setattr(self, key, getattr(self, key) + diff)

class Stats(BaseStats):
    hp = StatHelper('hp', MinMaxStat)
