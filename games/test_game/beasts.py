from nagm import engine
from .types import *
from .attacks import *

R = engine.stats.StatsRefs

class S(engine.stats.Stats):
    att = engine.stats.StatHelper('att', engine.stats.MinMaxStat)
    dfse = engine.stats.StatHelper('dfse', engine.stats.MinMaxStat)

bulbizarre = engine.beast.BeastFamily(id='001', name='Bulbizarre', type=plante, attacks=(charge, fouet_lianes, mimi_queue), stats_ref=R(S, hp=50, att=1, dfse=1))
salameche = engine.beast.BeastFamily(id='004', name='Salamèche', type=feu, attacks=(griffe, flameche, mimi_queue), stats_ref=R(S, hp=50, att=1, dfse=1))
carapuce = engine.beast.BeastFamily(id='007', name='Carapuce', type=eau, attacks=(charge, pistolet_a_o, mimi_queue), stats_ref=R(S, hp=50, att=1, dfse=1))
rattata = engine.beast.BeastFamily(id='019', name='Rattata', type=normal, attacks=(charge, griffe, mimi_queue), stats_ref=R(S, hp=50, att=1, dfse=1))
pikachu = engine.beast.BeastFamily(id='025', name='Pikachu', type=electrik, attacks=(charge, eclair, mimi_queue), stats_ref=R(S, hp=50, att=1, dfse=1))
