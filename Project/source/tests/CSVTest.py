import sys

sys.path.append("../")
from data_parsing.CSV_data_parser import *
from data_parsing.Planet import *
from data_parsing.PlanetaryObject import *
import unittest


class TestCSV_parser(unittest.TestCase):
    exo = "exoplanetEU_csv"
    nas = "nasa_csv"

    def testFullPlanetParsingEU(self):
        planets = buildListPlanetsAllField(self.exo, "eu")
        planet = planets[0]
        self.assertEqual(planet.data["semimajoraxis"], '0.5')
        self.assertEqual(planet.data["discoveryyear"], '2001')
        self.assertEqual(planet.name, "mars")
        self.verifyPlanet(planet)

    def testFullPlanetParsingNASA(self):
        planets = buildListPlanetsAllField(self.nas, "nasa")
        planet = planets[0]
        self.verifyPlanet(planet)
        self.assertEqual(planet.name, "mars a")

    def testStarParsingEU(self):
        stars = buildDictStarExistingField(self.exo, "eu")
        try:
            star = stars["sun"]
            mars = star.planetObjects[0]
            self.verifyPlanet(mars)
        except KeyError as err:
            self.fail(str(err))

    def testStarParsingNASA(self):
        stars = buildDictStarExistingField(self.nas, "nasa")
        try:
            star = stars["mars"]
            mars = star.planetObjects[0]
            self.verifyPlanet(mars)
        except KeyError as err:
            self.fail(str(err))

    def verifyPlanet(self, planet):
        data = planet.getData()
        self.assertEqual(data["mass"], '10')
        self.assertEqual(data["radius"], '3.14')
        self.assertEqual(data["period"], '0.7')
        self.assertEqual(data["eccentricity"], '1')
        self.assertEqual(data["discoverymethod"], "RV")


if __name__ == '__main__':
    unittest.main(exit=False)
