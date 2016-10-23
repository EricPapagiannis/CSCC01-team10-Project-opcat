from data_parsing.PlanetaryObject import *


class Planet(PlanetaryObject):

    def __init__(self, name):
        self.data = {"namePlanet": name}