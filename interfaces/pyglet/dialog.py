import pyglet
import engine.meta

@engine.meta.register('engine.dialog.Message')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__batch = None

    @property
    def batch(self):
        if self.__batch is None:
            self.__batch = pyglet.graphics.Batch()
            bg_img = pyglet.image.Texture.create(200, 30)
            #self.__sprite = pyglet.text.Sprite(bg_img, x=0, y=0, batch=self.__batch)
            self.__label = pyglet.text.Label(self.msg, batch=self.__batch)
        return self.__batch

@engine.meta.register('engine.dialog.Choice')
class _:
    currents = {}

    @classmethod
    def labels_hash(cls, labels):
        labels = hash(tuple(labels))
        return labels

    def __init__(self, **kwargs):
        kwargs.setdefault(
            'current',
            self.currents.get(self.labels_hash(kwargs['labels']), 0)
        )
        super().__init__(**kwargs)
        self.__batch = None

    @property
    def batch(self):
        if self.__batch is None:
            self.__size = len(self.labels)
            self.__batch = pyglet.graphics.Batch()
            self.__labels = [pyglet.text.Label(msg, x=100*i+10, batch=self.__batch) for i, msg in enumerate(self.labels)]
            self.__bullet = pyglet.text.Label('•', x=self.current * 100, batch=self.__batch)
        return self.__batch

    def select(self, player, d):
        self.batch # compute
        self.current = (self.current + d) % self.__size
        self.currents[self.labels_hash(self.labels)] = self.current
        self.__bullet.x = self.current * 100

    def handle_key(self, player, key):
        if key == pyglet.window.key.LEFT:
            self.select(player, -1)
        elif key == pyglet.window.key.RIGHT:
            self.select(player, 1)
