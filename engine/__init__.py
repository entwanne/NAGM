'''engine — Base classes for all game components
'''

__all__ = [
    'meta', 'resources', 'signals', 'bind', 'clock', # can be loaded before interface
    'game', 'gobject', 'map', 'battle', 'dialog', 'tile',
    'event', 'character', 'player', 'object',
    'type', 'attack', 'beast', 'stats', 'zone',
    'mixins',
]

def load_modules():
    'Load all engine modules'
    from importlib import import_module
    for modname in __all__:
        import_module('.' + modname, __package__)
