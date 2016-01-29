import pyglet
import engine.meta


@engine.meta.register('engine.game.Game')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = pyglet.window.Window(width=21*16, height=21*16)
        @self.window.event
        def on_expose():
            pass
        @self.window.event
        def on_draw():
            self.draw()
        @self.window.event
        def on_key_press(key, modifiers):
            self.key_press(key)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        from engine.clock import Clock
        tick = 0.3
        tick = 0.
        self.signals_clock = Clock(tick)
        self.keyboard_clock = Clock(tick)
        self.events_clock = Clock(tick)
        #pyglet.clock.schedule(self.update)
        pyglet.clock.schedule_interval(self.update, 0.1)

    def draw(self):
        self.window.clear()
        if self.player.battle:
            self.player.battle.batch.draw()
        elif self.player.map:
            sprite = self.player.sprites[0]
            dx = (self.window.width - sprite.width) // 2 - sprite.x
            dy = (self.window.height - sprite.height) // 2 - sprite.y
            pyglet.gl.glTranslatef(dx, dy, 0)
            self.player.map.batch.draw()
            pyglet.gl.glTranslatef(-dx, -dy, 0)
        if self.player.dialog:
            self.player.dialog.label.draw()

    def update(self, _dt):
        if self.have_signals():
            if self.signals_clock.finished:
                self.handle_signals()
                self.signals_clock.reset()
            return
        if self.events_clock.finished:
            self.step_events()
            self.events_clock.reset()
        if self.keyboard_clock.finished:
            dx, dy = 0, 0
            if self.keys.get(pyglet.window.key.LEFT):
                dx = -1
            elif self.keys.get(pyglet.window.key.RIGHT):
                dx = 1
            if self.keys.get(pyglet.window.key.UP):
                dy = 1
            elif self.keys.get(pyglet.window.key.DOWN):
                dy = -1
            if dx or dy:
                if self.player.direction == (dx, dy):
                    self.player.walk()
                else:
                    self.player.turn(dx, dy)
                self.signals_clock.reset()
                self.keyboard_clock.reset()

    def key_press(self, key):
        if key == pyglet.window.key.SPACE:
            self.player.action()
        elif key == pyglet.window.key.S:
            self.save('game.save')


    def run(self):
        pyglet.app.run()
