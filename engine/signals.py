signals = [] # queue of signals to handle

def send_signal(handler, obj, *args, **kwargs):
    signals.append((handler, obj, args, kwargs))

def handle_signals(game):
    for _ in range(len(signals)):
        handler, obj, args, kwargs = signals.pop(0)
        handler(game, obj, *args, **kwargs)

def have_signals():
    return bool(signals)
