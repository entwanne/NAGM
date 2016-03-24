from nagm.engine.attack import Attack
from nagm.engine.formula import Var, Min, Max, Cond
from .types import *
from math import floor

att = Var('s_att') / Var('r_dfse')
typ = Var('type_rapport')

def E(**kwargs):
    dic = {}
    for attr, value in kwargs.items():
        if attr.endswith('_add'):
            attr, _ = attr.rsplit('_add', 1)
            dic[attr] = floor(Var(attr) + value)
        elif attr.endswith('_sub'):
            attr, _ = attr.rsplit('_sub', 1)
            dic[attr] = floor(Var(attr) - value)
        else:
            dic[attr] = floor(value)
    return dic

mimi_queue = Attack(name='Mimi-queue', type=normal, effects=E(r_dfse_sub=1))
charge = Attack(name='Charge', type=normal, effects=E(r_hp_sub=10*att*typ))
griffe = Attack(name='Griffe', type=normal, effects=E(r_hp_sub=10*att*typ))
fouet_lianes = Attack(name='Fouet lianes', type=plante, effects=E(r_hp_sub=20*att*typ))
flameche = Attack(name='Flamèche', type=feu, effects=E(r_hp_sub=20*att*typ))
pistolet_a_o = Attack(name='Pistolet a O', type=eau, effects=E(r_hp_sub=20*att*typ))
eclair = Attack(name='Éclair', type=electrik, effects=E(r_hp_sub=20*att*typ))
faux_chage = Attack(name='Faux-chage', type=normal, effects=E(r_hp=Cond(Var('r_hp') > 1, Max(1, Var('r_hp')-10*att*typ), 0)))
soin = Attack(name='Soin', type=normal, effects=E(s_hp_add=50))
