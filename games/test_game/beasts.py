from nagm import engine
from .attacks import charge

pikachu = engine.beast.BeastFamily(name='Pikachu', type='Electrik')
carapuce = engine.beast.BeastFamily(name='Carapuce', type='Eau', attacks=(engine.attack.lutte, charge))
