registered = {}

class GObjectMeta(type):
    def __new__(cls, name, bases, dict):
        attributes = ()
        for base in bases:
            if isinstance(base, cls):
                attributes += base.__attributes__
        if '__attributes__' in dict:
            attributes += dict['__attributes__']
        dict['__attributes__'] = attributes
        return super().__new__(cls, name, bases, dict)

def apply(cls):
    if not isinstance(cls, GObjectMeta):
        return cls
    fullname = '{}.{}'.format(cls.__module__, cls.__qualname__)
    if fullname in registered:
        cls = type(cls.__name__,
                   (registered[fullname], cls),
                   {'__module__': cls.__module__, '__qualname__': cls.__qualname__}
        )
    return cls

def register(name):
    def decorator(cls):
        registered[name] = cls
        return cls
    return decorator
