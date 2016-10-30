from data_parsing.PlanetaryObject import *


class Star(PlanetaryObject):
    def __init__(self, name):
        self.data = {"nameStar": name}
        self.name = name
        self.systemObject = None
        self.planetObjects = []
        self.systemObjectNamesToSystem = dict()
        self.nameToPlanet = dict()
