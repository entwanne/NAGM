'''Game definitions (classes/functions)
Only this module should be loaded when using a game save
'''

from nagm import engine

class BourgChar(engine.mixins.characters.Speaker, engine.mixins.characters.InfiniteWalker, engine.character.Character):
    pass

class ActionEvent(engine.mixins.event.ActionEventCallback, engine.event.Event):
    pass

def add_player(game, name, map, position, *beasts_families):
    player = engine.player.Player.spawn(name=name, map=map, position=position)
    player.beastiary = engine.beast.Beastiary()
    player.beasts = [engine.beast.Beast.from_family(family) for family in beasts_families]
    from . import attacks
    for beast in player.beasts:
        beast.stats.att_iv = 15
        beast.stats.dfse_iv = 15
        beast.stats.hp_default = 1000
        beast.stats.hp = 1000
        beast.attacks.pop()
        #beast.attacks.append(attacks.faux_chage)
        beast.attacks.append(attacks.abime)
        beast.attacks.append(attacks.soin)
    # do it with Player.spawn ?
    game.players.append(player)

import random

class EVIVStat(engine.stats.Stat):
    def __init__(self, ev, iv, bonus):
        self.ev = ev
        self.iv = iv
        self.bonus = bonus
    def __iget__(self, instance):
        return getattr(instance, self.ev) + getattr(instance, self.iv) + getattr(instance, self.bonus)
    def __set__(self, instance, value):
        default = getattr(instance, self.ev) + getattr(instance, self.iv)
        setattr(instance, self.bonus, value - default)
    def defaults(self, kwargs):
        kwargs.setdefault(self.ev, 10)
        kwargs.setdefault(self.iv, random.randint(5, 15))
        kwargs.setdefault(self.bonus, 0)
    @property
    def attributes(self):
        return (self.ev, self.iv, self.bonus)

class Stats(engine.stats.Stats):
    hp = engine.stats.MinMaxStat('_hp', min=0, max='hp_default')
    hp_default = engine.stats.MinMaxStat('_hp_default', min=0)
    att = EVIVStat('att_ev', 'att_iv', 'att_bonus')
    att_bonus = engine.stats.MinMaxStat('_att_bonus', -10, 10)
    dfse = EVIVStat('dfse_ev', 'dfse_iv', 'dfse_bonus')
    dfse_bonus = engine.stats.MinMaxStat('_dfse_bonus', -10, 10)

    @property
    def hp_coef(self):
        return self.hp / self.hp_default

    def recompute(self):
        # ou remplacer par système de contextes avec fin
        # une attaque peut metre en place un ctx, qui prendra fin dans x tours (ou à la fin du combat)
        # -> mais plus difficile à gérer
        # (difficile car par exemple, il faut garder une référence vers la beast en cours pour pouvoir appliquer l'opération inverse)
        super().recompute()
        self.att_bonus = 0
        self.dfse_bonus = 0
        # + set flag for evolution

    # + method to win exp and ev when a beast is defeated

# Move to engine.mixins/engine.helpers
# -> rename to ParamEffect ?
class Effect:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __call__(self, attack, sender, target):
        return True

    @classmethod
    def make(cls, func):
        "Create a new effect-class inheriting from Effect and having its proper __call_ behaviour"
        # remove function from Effect class and add it to the effect/mixin module ?
        dic = {
            '__qualname__': func.__qualname__,
            '__module__': func.__module__,
            '__call__': func,
        }
        return type(func.__name__, (cls,), dic)

@Effect.make
def precision(effect, attack, sender, target):
    if random.random() < effect.prec:
        return True
    print('but failed')
    return False

@Effect.make
def stat(effect, attack, sender, target):
    value = getattr(target.stats, effect.stat)
    setattr(target.stats, effect.stat, value + effect.value)
    print('{}.{} = {}'.format(target.name, effect.stat, getattr(target.stats, effect.stat)))
    return True

@Effect.make
def heal(effect, attack, sender, target):
    target.stats.hp += effect.heal
    print('{}.hp = {}'.format(target.name, target.stats.hp))
    return True

@Effect.make
def offensive(effect, attack, sender, target):
    typ = attack.type.over(target.type)
    att = sender.stats.att / target.stats.dfse
    target.stats.hp -= int(effect.force * typ * att)
    print('{}.hp = {}'.format(target.name, target.stats.hp))
    return True

def faux_chage_effect(attack, sender, target):
    if target.stats.hp > 1:
        target.stats.hp = max(target.stats.hp - 40, 1)
    else:
        target.stats.hp = 0

# Effects should raise an Useable.Exit exception to exit battle (ball, teleport, hurlement, ...)
# Exit choice in battle menu can become an effect
# Beast-switching can also be an effect
# -> Add facility to create an Useable-Effect (which is an unseable and an effect at the same time) -> or just have some Useable instances exit and switch
# exit and swith will be useables owned by battle instance

@Effect.make
def capture(effect, ball, sender, target):
    # manage distance between sender and target
    # (= ||sender.position - target.position||), or distance²
    # -> by a precision effect ? (it would be reused for potions for example)
    sender.beasts.append(target)
