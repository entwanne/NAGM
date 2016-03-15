from nagm import engine
from .attacks import lutte, charge

pikachu = engine.beast.BeastFamily(id='025', name='Pikachu', type='Electrik', attacks=(lutte,))
carapuce = engine.beast.BeastFamily(id='007', name='Carapuce', type='Eau', attacks=(lutte, charge))
