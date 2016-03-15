from nagm import engine
from .attacks import *

bulbizarre = engine.beast.BeastFamily(id='001', name='Bulbizarre', type='Plante', attacks=(charge, fouet_lianes))
salameche = engine.beast.BeastFamily(id='004', name='Salamèche', type='Feu', attacks=(griffe, flameche))
carapuce = engine.beast.BeastFamily(id='007', name='Carapuce', type='Eau', attacks=(charge, pistolet_a_o))
rattata = engine.beast.BeastFamily(id='019', name='Rattata', type='Normal', attacks=(charge, griffe))
pikachu = engine.beast.BeastFamily(id='025', name='Pikachu', type='Electrik', attacks=(charge, eclair))
