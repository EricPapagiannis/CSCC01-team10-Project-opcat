from data_parsing.PlanetaryObject import *


class System(PlanetaryObject):
    def __init__(self, name):
        # data fields in the system
        # self.data = {"nameSystem": name}
        self.data = dict()
        # the main name of the system
        self.name = self._fixStr(name)
        # a list of star objects in the system
        self.starObjects = []
        # a dict mapping the star names (and alternate names) to the star
        # objects in the system
        self.nameToStar = dict()
        self.otherNamesSystem = []
        self.errors = dict()
        self.lastupdate = "00/00/00"
