registered = {}

class GObjectMeta(type):
    def __new__(cls, name, bases, dict):
        c = super().__new__(cls, name, bases, dict)
        qualname = '{}.{}'.format(c.__module__, c.__qualname__)
        if qualname in registered:
            print(cls, qualname)
            c = type(name, (registered[qualname], c), {})
        return c

def register(name):
    def decorator(cls):
        registered[name] = cls
        return cls
    return decorator
