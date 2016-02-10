import pyglet
import engine.meta

@engine.meta.register('engine.dialog.Message')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = None

    def draw(self):
        if not self.label:
            self.label = pyglet.text.Label(self.msg)
        self.label.draw()

@engine.meta.register('engine.dialog.Choice')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch = None

    def compute(self):
        if self.batch is not None:
            return
        self.size = len(self.choices)
        self.batch = pyglet.graphics.Batch()
        self.labels = [pyglet.text.Label(msg, x=100*i+10, batch=self.batch) for i, msg in enumerate(self.choices)]
        self.bullet = pyglet.text.Label('•', batch=self.batch)

    def draw(self):
        self.compute()
        self.batch.draw()

    def select(self, d):
        self.compute()
        self.current = (self.current + d) % self.size
        self.bullet.x = self.current * 100

    def handle_key(self, key):
        if key == pyglet.window.key.LEFT:
            self.select(-1)
        elif key == pyglet.window.key.RIGHT:
            self.select(1)
