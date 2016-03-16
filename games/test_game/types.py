from nagm import engine

plante = engine.type.Type(name='Plante')
feu = engine.type.Type(name='Feu')
eau = engine.type.Type(name='Eau')
electrik = engine.type.Type(name='Electrik')
normal = engine.type.Type(name='Normal')

from itertools import product

_types = (plante, feu, eau, electrik, normal)
_table = (
    ( 1, .5,  2,  1,  1),
    ( 2,  1, .5,  1,  1),
    (.5,  2,  1,  1,  1),
    ( 1, .5,  2,  1,  1),
    ( 1,  1,  1,  1,  1),
)
for (i, t1), (j, t2) in product(enumerate(_types), enumerate(_types)):
    t1.set_over(t2, _table[i][j])
