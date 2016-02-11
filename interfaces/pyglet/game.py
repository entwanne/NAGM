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

        self._ui_player = None

    @property
    def ui_player(self):
        if not self._ui_player:
            self._ui_player = self.players[0]
        return self._ui_player

    def draw(self):
        p = self.ui_player
        self.window.clear()
        if p.battle:
            p.battle.batch.draw()
        elif p.map:
            sprite = p.sprites[0]
            dx = (self.window.width - sprite.width) // 2 - sprite.x
            dy = (self.window.height - sprite.height) // 2 - sprite.y
            pyglet.gl.glTranslatef(dx, dy, 0)
            p.map.batch.draw()
            pyglet.gl.glTranslatef(-dx, -dy, 0)
        if p.dialog:
            p.dialog.draw()

    def update(self, _dt):
        if self.have_signals():
            if self.signals_clock.finished:
                self.handle_signals()
                self.signals_clock.reset()
            return
        if self.events_clock.finished:
            self.step()
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
                p = self.ui_player
                if p.direction == (dx, dy):
                    p.walk()
                else:
                    p.turn(dx, dy)
                self.signals_clock.reset()
                self.keyboard_clock.reset()

    def key_press(self, key):
        p = self.ui_player
        if p.dialog and hasattr(p.dialog, 'handle_key'):
            p.dialog.handle_key(key)
        if key == pyglet.window.key.SPACE:
            p.action()
        elif key == pyglet.window.key.S:
            self.save('game.save')
        elif key == pyglet.window.key.P:
            i = self.players.index(self._ui_player)
            i = (i + 1) % len(self.players)
            self._ui_player = self.players[i]
        elif key == pyglet.window.key.G:
            if p.ghost:
                p.pop_ghost()
            else:
                p.ghostify()

    def run(self):
        pyglet.app.run()
