import engine
from ..tiles import make_tiles
from ..zones import zone

tiles = []
tiles.append("""
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||x=xxxx||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||..**..||||
||||<.....||||
""")
tiles.append("""
||||......||||
||||......||||
||||......||||
||||......||||
||||......||||
||||......||||
||||......||||
||||......||||
||||-#----||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
||||      ||||
""")
tiles = make_tiles(tiles)
zones = [zone]
map = engine.map.Map.from_tiles(tiles, zones)
