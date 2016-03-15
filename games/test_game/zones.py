from nagm import engine
from .beasts import *

pikagroup = engine.zone.WildGroup(family=pikachu, population=5) # group of 10 pikachus
caragroup = engine.zone.WildGroup(family=carapuce, population=2) # group of 4 carapuces
zone = engine.zone.Zone(type='grass', groups=[pikagroup, caragroup])
