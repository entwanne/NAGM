from .gobject import GObject
from . import meta
from .meta import GObjectMeta

class Stat:
    is_attribute = False
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.__iget__(instance)
    def __iget__(self, instance):
        raise NotImplementedError
    def __set__(self, instance, value):
        raise AttributeError("can't set attribute")
    def defaults(self, kwargs):
        pass
    @property
    def attributes(self):
        return ()

class ValueStat(Stat):
    is_attribute = True
    def __init__(self, attr):
        super().__init__()
        self.attr = attr
    def __iget__(self, instance):
        return getattr(instance, self.attr)
    def __set__(self, instance, value):
        setattr(instance, self.attr, value)

class MinMaxStat(ValueStat):
    def __init__(self, attr, min=None, max=None):
        super().__init__(attr)
        self.min = min
        self.max = max
    @staticmethod
    def check(instance, value, ref_value, func):
        if ref_value is not None:
            if isinstance(ref_value, str):
                # no check if ref_value is not set in instance
                ref_value = getattr(instance, ref_value, value)
            value = func(value, ref_value)
        return value
    def __set__(self, instance, value):
        value = self.check(instance, value, self.min, max)
        value = self.check(instance, value, self.max, min)
        super().__set__(instance, value)

class StatsMeta(GObjectMeta):
    def __new__(cls, name, bases, dict):
        attributes = set(dict.pop('__attributes__', ()))
        stats = set(dict.pop('__stats__', ()))
        for base in bases:
            if isinstance(base, cls):
                stats.update(base.__stats__)
        for attr, value in dict.items():
            if isinstance(value, Stat):
                if value.is_attribute:
                    attributes.add(attr)
                attributes.update(value.attributes)
                stats.add(attr)
        dict['__attributes__'] = attributes
        dict['__stats__'] = stats
        return super().__new__(cls, name, bases, dict)

@meta.apply
class BaseStats(GObject, metaclass=StatsMeta):
    @classmethod
    def from_values(cls, **kwargs):
        for stat_name in cls.__stats__:
            stat = getattr(cls, stat_name)
            # __stats__ contains all Stat instances, but not only
            if isinstance(stat, Stat):
                stat.defaults(kwargs)
        return cls(**kwargs)

    @property
    def values(self):
        "Visible stats of the beast"
        return {stat: getattr(self, stat) for stat in self.__stats__}

    def apply(self, stats):
        for key, value in stats.items():
            setattr(self, key, value)

@meta.apply
class Stats(BaseStats):
    hp = MinMaxStat('_hp', min=0)

    @property
    def hp_coef(self):
        return min(self.hp, 1)

class StatsRef:
    def __init__(self, cls, **kwargs):
        self.cls = cls
        self.kwargs = kwargs

    def stats(self):
        return self.cls.from_values(**self.kwargs)
