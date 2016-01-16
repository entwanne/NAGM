signals = [] # queue of signals to handle
handlers = {}
def reg_signal(sigtype, callback):
    handlers.setdefault(sigtype, []).append(callback)
def handle_signals():
    #while signals:
    #    sigtype, *params = signals.pop(0)
    #    for handler in handlers.get(sigtype, ()):
    #        handler(sigtype, *params)
    for _ in range(len(signals)):
        sigtype, *params = signals.pop(0)
        for handler in handlers.get(sigtype, ()):
            handler(sigtype, *params)
def have_signals():
    return bool(signals)
