registered = {}

class GObjectMeta(type):
    pass

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
