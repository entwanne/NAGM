import os.path

path = [os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res'))]

def exists(name):
    for p in path:
        fullpath = os.path.join(p, name)
        if os.path.exists(fullpath):
            return fullpath
    return None

def get(name):
    fullpath = exists(name)
    if fullpath is None:
        raise FileNotFoundError('Resource {} not found'.format(repr(name)))
    return fullpath