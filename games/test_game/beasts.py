from nagm import engine
from .types import *
from .attacks import *

class Stats(engine.stats.Stats):
    att = engine.stats.StatHelper('att', engine.stats.MinMaxStat)
    dfse = engine.stats.StatHelper('dfse', engine.stats.MinMaxStat)

refs = engine.stats.StatsRefs(
    Stats,
    hp=100,
    att=20, att_min=1, att_max=255,
    dfse=20, dfse_min=1, dfse_max=255,
)

bulbizarre = engine.beast.BeastFamily(id='001', name='Bulbizarre', type=plante, attacks=(charge, fouet_lianes, mimi_queue), stats_ref=refs)
salameche = engine.beast.BeastFamily(id='004', name='Salamèche', type=feu, attacks=(griffe, flameche, mimi_queue), stats_ref=refs)
carapuce = engine.beast.BeastFamily(id='007', name='Carapuce', type=eau, attacks=(charge, pistolet_a_o, mimi_queue), stats_ref=refs)
rattata = engine.beast.BeastFamily(id='019', name='Rattata', type=normal, attacks=(charge, griffe, mimi_queue), stats_ref=refs)
pikachu = engine.beast.BeastFamily(id='025', name='Pikachu', type=electrik, attacks=(charge, eclair, mimi_queue), stats_ref=refs)
