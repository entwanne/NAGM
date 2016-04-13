from nagm.engine.meta import register as metareg

@metareg('nagm.engine.event.Event')
class _:
    sprites = ()

    def remove(self):
        super().remove()
        self.invalidate_ui()
