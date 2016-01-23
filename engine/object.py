from .event import Event
from . import meta

@meta.apply
class Object(Event):
    "All objects (can be found on the map, put in the bag)"
