signals = [] # queue of signals to handle

def send_signal(handler, obj, *args, **kwargs):
    '''Send a signal from a game objet to an handler
    <=> Append a callback to a queue'''
    signals.append((handler, obj, args, kwargs))

def _call_handler(handler, game, sender, args, kwargs):
    if is_sighandler(handler):
        handler(game, sender, *args, **kwargs)
    else:
        handler(*args, **kwargs)

def handle_signals(game):
    'Execute signal-callbacks currently in the queue'
    for _ in range(len(signals)):
        handler, sender, args, kwargs = signals.pop(0)
        _call_handler(handler, game, sender, args, kwargs)

def have_signals():
    'True if queue contains signals'
    return bool(signals)

def sighandler(f):
    '''Decorator to crate a signal handler.
    sighandlers will receive `game` and `sender` as first parameters'''
    f.is_sighandler = True
    return f

def is_sighandler(f):
    'True if a function is a sighandler'
    return getattr(f, 'is_sighandler', None)

@sighandler
class chain:
    'Chain several handlers for a same signal'

    def __init__(self, *handlers):
        self.handlers = handlers
    def __call__(self, game, sender, *args, **kwargs):
        for handler in self.handlers:
            _call_handler(handler, game, sender, args, kwargs)
