from data_parsing.PlanetaryObject import *


class System(PlanetaryObject):
    def __init__(self, name):
        self.data = {"nameSystem": name}
