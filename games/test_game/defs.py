from nagm import engine

class BourgChar(engine.mixins.characters.Speaker, engine.mixins.characters.InfiniteWalker, engine.character.Character):
    pass

class ActionEvent(engine.mixins.event.ActionEventCallback, engine.event.Event):
    pass

def add_player(game, name, map, position, *beasts_families):
    player = engine.player.Player(name=name, map=map, position=position)
    player.beastiary = engine.beast.Beastiary()
    player.beasts = [engine.beast.Beast.from_family(family) for family in beasts_families]
    from .attacks import faux_chage, soin
    for beast in player.beasts:
        beast.stats.att_iv = 15
        beast.stats.dfse_iv = 15
        beast.stats.hp_default = 1000
        beast.stats.hp = 1000
        beast.attacks.pop()
        beast.attacks.append(faux_chage)
        beast.attacks.append(soin)
    game.players.append(player)
    game.events.append(player)
