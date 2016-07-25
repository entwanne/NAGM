import os.path

path = [os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res'))]

def exists(name):
    'Return True if a resource exists'
    for p in path:
        fullpath = os.path.join(p, name)
        if os.path.exists(fullpath):
            return fullpath
    return None

def get(name):
    'Get path of a resource'
    fullpath = exists(name)
    if fullpath is None:
        raise FileNotFoundError('Resource {!r} not found'.format(name))
    return fullpath
