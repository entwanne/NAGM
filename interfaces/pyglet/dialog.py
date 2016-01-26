import pyglet
import engine.meta

@engine.meta.register('engine.dialog.Message')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = pyglet.text.Label(self.msg)
