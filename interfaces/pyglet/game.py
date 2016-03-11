import pyglet
import engine.meta


@engine.meta.register('engine.game.Game')
class _:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__window = pyglet.window.Window(width=21*16, height=21*16)
        @self.__window.event
        def on_expose():
            pass
        @self.__window.event
        def on_draw():
            self.__draw()
        @self.__window.event
        def on_key_press(key, modifiers):
            self.__key_press(key)
        self.__keys = pyglet.window.key.KeyStateHandler()
        self.__window.push_handlers(self.__keys)

        from engine.clock import Clock
        tick = 0.3
        tick = 0.
        self.__signals_clock = Clock(tick)
        self.__keyboard_clock = Clock(tick)
        self.__events_clock = Clock(tick)
        pyglet.clock.schedule_interval(self.__update, 0.1)

        self.__ui_player = None

    @property
    def ui_player(self):
        if not self.__ui_player:
            self.__ui_player = self.players[0]
        return self.__ui_player

    def __draw(self):
        if engine.gobject.GObject.to_refresh:
            to_refresh, engine.gobject.GObject.to_refresh = engine.gobject.GObject.to_refresh, []
            for obj in to_refresh:
                obj.refresh_ui()
        p = self.ui_player
        self.__window.clear()
        if p.map:
            dx, dy = p.map.get_translation(self.__window, p)
            pyglet.gl.glTranslatef(dx, dy, 0)
            p.map.batch.draw()
            pyglet.gl.glTranslatef(-dx, -dy, 0)
        if p.dialog and hasattr(p.dialog, 'batch'):
            p.dialog.batch.draw()

    def __update(self, _dt):
        if self.have_signals():
            if self.__signals_clock.finished:
                self.handle_signals()
                self.__signals_clock.reset()
        if self.__events_clock.finished:
            self.step()
            self.__events_clock.reset()
        if self.__keyboard_clock.finished:
            dx, dy = 0, 0
            if self.__keys.get(pyglet.window.key.LEFT):
                dx = -1
            elif self.__keys.get(pyglet.window.key.RIGHT):
                dx = 1
            if self.__keys.get(pyglet.window.key.UP):
                dy = 1
            elif self.__keys.get(pyglet.window.key.DOWN):
                dy = -1
            if dx or dy:
                p = self.ui_player
                if p.direction == (dx, dy):
                    p.walk()
                else:
                    p.turn(dx, dy)
                self.__signals_clock.reset()
                self.__keyboard_clock.reset()

    def __key_press(self, key):
        p = self.ui_player
        if p.dialog and hasattr(p.dialog, 'handle_key'):
            p.dialog.handle_key(p, key)
        if key == pyglet.window.key.SPACE:
            p.action()
        elif key == pyglet.window.key.S:
            self.save('game.save')
        elif key == pyglet.window.key.P:
            i = self.players.index(self.__ui_player)
            i = (i + 1) % len(self.players)
            self.__ui_player = self.players[i]
        elif key == pyglet.window.key.G:
            if p.ghost:
                p.pop_ghost()
            else:
                p.ghostify()

    def run(self):
        pyglet.app.run()
