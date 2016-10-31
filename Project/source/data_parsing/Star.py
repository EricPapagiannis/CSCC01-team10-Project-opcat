from data_parsing.PlanetaryObject import *


class Star(PlanetaryObject):
    def __init__(self, name):
        # data fields in the star
        self.data = {"nameStar": name}
        # main name of the star
        self.name = name
        # the system the star is in
        self.systemObject = None
        # a list of planet objects in the star
        self.planetObjects = []
        # a dict mapping the name of the system and its alternate names to the
        # object that the star is in
        self.systemObjectNamesToSystem = dict()
        # a dict mapping the planet names (and alternate names) to the planet
        # objects in the star
        self.nameToPlanet = dict()
