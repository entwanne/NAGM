from nagm import engine
from .types import *
from .attacks import *

bulbizarre = engine.beast.BeastFamily(id='001', name='Bulbizarre', type=plante, attacks=(charge, fouet_lianes))
salameche = engine.beast.BeastFamily(id='004', name='Salamèche', type=feu, attacks=(griffe, flameche))
carapuce = engine.beast.BeastFamily(id='007', name='Carapuce', type=eau, attacks=(charge, pistolet_a_o))
rattata = engine.beast.BeastFamily(id='019', name='Rattata', type=normal, attacks=(charge, griffe))
pikachu = engine.beast.BeastFamily(id='025', name='Pikachu', type=electrik, attacks=(charge, eclair))
