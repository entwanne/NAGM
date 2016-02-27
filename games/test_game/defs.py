import engine
from engine.signals import sighandler
from engine import bind

class BourgChar(engine.mixins.characters.Speaker, engine.mixins.characters.InfiniteWalker, engine.character.Character):
    pass

class ActionEvent(engine.mixins.event.ActionEventCallback, engine.event.Event):
    pass

def add_player(game, name, map, position, beast_family):
    player = engine.player.Player(name=name, map=map, position=position)
    player.beastiary = engine.beast.Beastiary()
    player.beast = engine.beast.Beast(family=beast_family, dfse=10)
    game.players.append(player)
    game.events.append(player)
