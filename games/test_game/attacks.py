from nagm.engine.attack import Attack
from nagm.engine.formula import Var
from .types import *

att = Var('s_att') / Var('r_dfse')
typ = Var('type_rapport')

mimi_queue = Attack(name='Mimi-queue', type=normal, effects={})
charge = Attack(name='Charge', type=normal, effects={'r_hp': -10*att*typ})
griffe = Attack(name='Griffe', type=normal, effects={'r_hp': -10*att*typ})
fouet_lianes = Attack(name='Fouet lianes', type=plante, effects={'r_hp': -20*att*typ})
flameche = Attack(name='Flamèche', type=feu, effects={'r_hp': -20*att*typ})
pistolet_a_o = Attack(name='Pistolet a O', type=eau, effects={'r_hp': -20*att*typ})
eclair = Attack(name='Éclair', type=electrik, effects={'r_hp': -20*att*typ})
