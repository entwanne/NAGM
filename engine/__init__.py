__all__ = [
    'meta',
    'game', 'event', 'beast', 'character', 'object', 'zone',
    'map', 'tile', 'player', 'battle', 'dialog', 'signals', 'bind',
]

def load_modules():
    from importlib import import_module
    for modname in __all__:
        import_module('.' + modname, __package__)
