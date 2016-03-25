from nagm.engine.attack import Attack
from .types import *
from .defs import precision, stat, heal, offensive, faux_chage_effect

prec = precision(prec=0.9)
mimi_queue = Attack(name='Mimi-queue', type=normal, effects=(prec, stat(stat='dfse', value=-1),))
charge = Attack(name='Charge', type=normal, effects=(prec, offensive(force=10),))
griffe = Attack(name='Griffe', type=normal, effects=(prec, offensive(force=10),))
fouet_lianes = Attack(name='Fouet lianes', type=plante, effects=(prec, offensive(force=20),))
flameche = Attack(name='Flamèche', type=feu, effects=(prec, offensive(force=20),))
pistolet_a_o = Attack(name='Pistolet à o', type=eau, effects=(prec, offensive(force=20),))
eclair = Attack(name='Éclair', type=electrik, effects=(prec, offensive(force=20),))
soin = Attack(name='Soin', type=normal, effects=(prec, heal(heal=50),), reflexive=True)
abime = Attack(name='Abîme', type=normal, effects=(precision(prec=0.1), offensive(force=1000),))
faux_chage = Attack(name='Faux-chage', type=normal, effects=(prec, faux_chage_effect,))
