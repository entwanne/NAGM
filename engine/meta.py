registered = {}
created = {}

class GObjectMeta(type):
    def __new__(cls, name, bases, dict):
        c = super().__new__(cls, name, bases, dict)

        # Do not handle classes that are already decorated
        if c.__module__.startswith('<meta>'):
            return c

        # Fullname of the class (base module + qualified name)
        fullname = '{}.{}'.format(c.__module__, c.__qualname__)

        # Decorate registered classes
        if fullname in registered:
            print(cls, fullname)
            c = type(name,
                     (registered[fullname], c),
                     {'__module__': '<meta>.{}'.format(fullname)})

        # Set fullname, save class and return
        c.__fullname__ = fullname
        created[fullname] = c
        return c

def register(name):
    def decorator(cls):
        registered[name] = cls
        return cls
    return decorator
