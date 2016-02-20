import engine
from engine.signals import sighandler
from engine import bind

class BourgChar(engine.mixins.characters.Speaker, engine.mixins.characters.InfiniteWalker, engine.character.Character):
    pass
