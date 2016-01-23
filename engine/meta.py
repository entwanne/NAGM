registered = {}
created = {}

class GObjectMeta(type):
    def __new__(cls, name, bases, dict):
        c = super().__new__(cls, name, bases, dict)
        fullname = '{}.{}'.format(c.__module__, c.__qualname__)
        c.__fullname__ = fullname
        created[fullname] = c
        return c

def apply(cls):
    if not isinstance(cls, GObjectMeta):
        return cls
    if cls.__fullname__ in registered:
        cls = type(cls.__name__,
                   (registered[cls.__fullname__], cls),
                   {'__module__': cls.__module__, '__qualname__': cls.__qualname__}
        )
    return cls

def register(name):
    def decorator(cls):
        registered[name] = cls
        return cls
    return decorator
