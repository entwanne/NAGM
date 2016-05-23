registered = {}

class GObjectMeta(type):
    '''Metaclass of all game objects
    Useful to easily replace engine classes by UI ones
    '''

    def __new__(cls, name, bases, dict):
        attributes = set(dict.pop('__attributes__', ()))
        for base in bases:
            if isinstance(base, cls):
                attributes.update(base.__attributes__)
        dict['__attributes__'] = attributes
        return super().__new__(cls, name, bases, dict)

def apply(cls):
    '''Decorator to apply a register mixin on an engine class
    Create a new class that inherits from engine class and from the mixin'''
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
    'Decorator to register a mixin-class (UI)'
    def decorator(cls):
        # + add possibility to patch a class several times ?
        # (to add behaviours specific to a game, or to enable a nuzlock mode for example)
        registered[name] = cls
        return cls
    return decorator
