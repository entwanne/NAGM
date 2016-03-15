from nagm import engine
from .attacks import charge

pikachu = engine.beast.BeastFamily(id='025', name='Pikachu', type='Electrik')
carapuce = engine.beast.BeastFamily(id='007', name='Carapuce', type='Eau', attacks=(engine.attack.lutte, charge))
