from parsing.PlanetaryObject import *


class Star(PlanetaryObject):
    def __init__(self, name):
        self.data = {"nameStar": name}
