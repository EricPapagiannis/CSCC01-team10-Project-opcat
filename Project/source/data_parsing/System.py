from data_parsing.PlanetaryObject import *


class System(PlanetaryObject):
    def __init__(self, name):
        # data fields in the system
        self.data = {"nameSystem": name}
        # the main name of the system
        self.name = name
        # a list of star objects in the system
        self.starObjects = []
        # a dict mapping the star names (and alternate names) to the star
        # objects in the system
        self.nameToStar = dict()
