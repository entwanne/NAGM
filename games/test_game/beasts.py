from nagm import engine
from .types import *
from .attacks import *

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

refs = engine.stats.StatsRef(
    Stats,
    hp=100,
    hp_default=100,
)

bulbizarre = engine.beast.BeastFamily(id='001', name='Bulbizarre', type=plante, attacks=(charge, fouet_lianes, mimi_queue), stats_ref=refs)
salameche = engine.beast.BeastFamily(id='004', name='Salamèche', type=feu, attacks=(griffe, flameche, mimi_queue), stats_ref=refs)
carapuce = engine.beast.BeastFamily(id='007', name='Carapuce', type=eau, attacks=(charge, pistolet_a_o, mimi_queue), stats_ref=refs)
rattata = engine.beast.BeastFamily(id='019', name='Rattata', type=normal, attacks=(charge, griffe, mimi_queue), stats_ref=refs)
pikachu = engine.beast.BeastFamily(id='025', name='Pikachu', type=electrik, attacks=(charge, eclair, mimi_queue), stats_ref=refs)
