from nagm import engine

class BourgChar(engine.mixins.characters.Speaker, engine.mixins.characters.InfiniteWalker, engine.character.Character):
    pass

class ActionEvent(engine.mixins.event.ActionEventCallback, engine.event.Event):
    pass

def add_player(game, name, map, position, *beasts_families):
    player = engine.player.Player(name=name, map=map, position=position)
    player.beastiary = engine.beast.Beastiary()
    player.beasts = [engine.beast.Beast.from_family(family) for family in beasts_families]
    for beast in player.beasts:
        beast.stats.dfse.max = 10
        beast.stats.dfse.reset()
    game.players.append(player)
    game.events.append(player)
