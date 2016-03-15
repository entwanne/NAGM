__all__ = [
    'meta', 'resources', 'signals', 'bind', 'clock', # can be loaded before interface
    'game', 'event', 'beast', 'character', 'object', 'zone',
    'map', 'tile', 'player', 'battle', 'dialog', 'mixins',
]

def load_modules():
    from importlib import import_module
    for modname in __all__:
        import_module('.' + modname, __package__)
