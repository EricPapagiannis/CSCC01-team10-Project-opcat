from data_parsing.PlanetaryObject import * 
#from PlanetaryObject import *

class Planet(PlanetaryObject):
    def __init__(self, name):
        # data fields in the planet
        self.data = {"namePlanet": name}
        # the main name of the planet
        self.name = name
        # the star the planet is in
        self.starObject = None
        # a dict mapping the name of the star and its alternate names to the
        # object that the planet is in
        self.starObjectNamesToStar = dict()