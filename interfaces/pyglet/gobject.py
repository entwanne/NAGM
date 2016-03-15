from nagm.engine.meta import register as metareg

@metareg('nagm.engine.gobject.GObject')
class _:
    to_refresh = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, 'refresh_ui'):
            self.invalidate_ui()

    def invalidate_ui(self):
        self.to_refresh.append(self)