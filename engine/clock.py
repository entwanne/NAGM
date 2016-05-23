import time

class Clock:
    'Measure time (timer)'

    def __init__(self, max=None):
        self.reset()
        self.max = max

    def reset(self):
        'Reset timer'
        self.time = time.time()

    @property
    def elapsed(self):
        'Get number of seconds elapsed since last reset'
        return time.time() - self.time

    @property
    def finished(self):
        'True if a max number of seconds has been reached'
        if self.max is None:
            return False
        return self.elapsed > self.max

    def __getstate__(self):
        return {'elapsed': self.elapsed, 'max': self.max}

    def __setstate__(self, state):
        self.max = state['max']
        self.time = time.time() - state['elapsed']
