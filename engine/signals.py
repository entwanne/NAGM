signals = [] # queue of signals to handle

def send_signal(handler, obj, *args, **kwargs):
    signals.append((handler, obj, args, kwargs))

def handle_signals(game):
    for _ in range(len(signals)):
        handler, sender, args, kwargs = signals.pop(0)
        if is_sighandler(handler):
            handler(game, sender, *args, **kwargs)
        else:
            handler(*args, **kwargs)

def have_signals():
    return bool(signals)

def sighandler(f):
    "sighandlers will receive `game` and `sender` first parameters"
    f.is_sighandler = True
    return f

def is_sighandler(f):
    return getattr(f, 'is_sighandler', None)
