from data_parsing.PlanetaryObject import *


class Planet(PlanetaryObject):
    def __init__(self, name):
        # data fields in the planet
        # self.data = {"namePlanet": name}
        self.data = dict()
        # the main name of the planet
        self.name = self._fixStr(name)
        # the star the planet is in
        self.nameStar = ""
        self.starObject = None
        # a dict mapping the name of the star and its alternate names to the
        # object that the planet is in
        self.starObjectNamesToStar = dict()
        self.otherNamesPlanet = []
        self.errors = dict()
        self.lastupdate = "00/00/00"
