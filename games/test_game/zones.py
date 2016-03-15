from nagm import engine
from .beasts import *

groups = (
    engine.zone.WildGroup(family=bulbizarre, population=1),
    engine.zone.WildGroup(family=salameche, population=1),
    engine.zone.WildGroup(family=carapuce, population=1),
    engine.zone.WildGroup(family=rattata, population=3),
    engine.zone.WildGroup(family=pikachu, population=1),
)
zone = engine.zone.Zone(type='grass', groups=groups)
