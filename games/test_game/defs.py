import engine
from engine.signals import sighandler
from engine import bind

@engine.meta.apply
class BourgChar(engine.mixins.characters.Speaker, engine.mixins.characters.InfiniteWalker, engine.character.Character):
    def __init__(self, **kwargs):
        if not 'dialogs' in kwargs:
            kwargs['dialogs'] = (
                engine.dialog.Message(msg='Hello'),
                engine.dialog.Message(msg='World'),
                engine.dialog.Message(msg='!'),
            )
        super().__init__(**kwargs)

class BourgChar2(BourgChar):
    def __init__(self, **kwargs):
        if not 'dialogs' in kwargs:
            message = engine.dialog.Message(msg='cool')
            kwargs['dialogs'] = (
                engine.dialog.Choice(
                    choices=('oui', 'non'),
                    signals=(bind.cb(self.say, bind._, message), None)
                ),
            )
        super().__init__(**kwargs)
