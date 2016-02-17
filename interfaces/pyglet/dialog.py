import pyglet
import engine.meta

@engine.meta.register('engine.dialog.Message')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.__label = None
        self.__batch = None

    #def draw(self):
    #    if not self.__label:
    #        self.__label = pyglet.text.Label(self.msg)
    #    self.__label.draw()

    @property
    def batch(self):
        if self.__batch is None:
            self.__batch = pyglet.graphics.Batch()
            self.__label = pyglet.text.Label(self.msg, batch=self.__batch)
        return self.__batch

@engine.meta.register('engine.dialog.Choice')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__batch = None

    @property
    def batch(self):
        if self.__batch is None:
            self.__size = len(self.choices)
            self.__batch = pyglet.graphics.Batch()
            self.__labels = [pyglet.text.Label(msg, x=100*i+10, batch=self.__batch) for i, msg in enumerate(self.choices)]
            self.__bullet = pyglet.text.Label('•', batch=self.__batch)
        return self.__batch

    def select(self, d):
        self.batch # compute
        self.current = (self.current + d) % self.__size
        self.__bullet.x = self.current * 100

    def handle_key(self, key):
        if key == pyglet.window.key.LEFT:
            self.select(-1)
        elif key == pyglet.window.key.RIGHT:
            self.select(1)
