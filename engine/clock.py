import time

class Clock:
    def __init__(self, max=None):
        self.reset()
        self.max = max

    def reset(self):
        self.time = time.time()

    @property
    def elapsed(self):
        return time.time() - self.time

    @property
    def finished(self):
        if self.max is None:
            return False
        return self.elapsed > self.max

    def __getstate__(self):
        return {'elapsed': self.elapsed, 'max': self.max}

    def __setstate__(self, state):
        self.max = state['max']
        self.time = time.time() - state['elapsed']
