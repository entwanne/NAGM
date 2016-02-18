import engine
from engine.signals import sighandler
from engine import bind

@engine.meta.apply
class BourgChar(engine.mixins.characters.Speaker, engine.mixins.characters.InfiniteWalker, engine.character.Character):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialogs = [
            engine.dialog.Message(msg='Hello'),
            engine.dialog.Message(msg='World'),
            engine.dialog.Message(msg='!', signal=bind.cb(self.set, moving=True)),
        ]

class BourgChar2(BourgChar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sig = bind.cb(self.set, moving=True)
        self.__message = engine.dialog.Message(msg='cool', signal=sig)
        self.dialogs = [
            engine.dialog.Choice(
                choices=('oui', 'non'),
                signals=(bind.cb(engine.dialog.spawn, bind._, self.__message), sig),
            )
        ]
