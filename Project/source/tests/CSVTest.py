from data_parsing.CSV_data_parser import *
from data_parsing.Planet import *
from data_parsing.PlanetaryObject import *
import unittest

class TestCSV_parser(unittest.TestCase):
    exo = "exoplanetEU_csv"
    nas = "nasa_csv"
    def testFullPlanetParsingEU():
            planets = buildListPlanets(exo,["mass","radius","period","semimajoraxis","eccentricity",
                    "discoverymethod","discoveryyear","lastupdate"], "eu")
            planet = planets[0]
            verifyPlanet(planet)
            

    def testFullPlanetParsingNASA():
            planets = buildListPlanets(nas,["mass","radius","period","semimajoraxis","eccentricity",
                    "discoverymethod","discoveryyear","lastupdate"], "nasa")
            planet = planets[0]
            verifyPlanet(planet)

    def testStarParsingEU():
            stars = buildDictStarExistingField(exo, "eu")
            try:
                    star = stars["sun"]
                    mars = star.planetObjects["mars"]
                    verifyPlanet(mars)
            except KeyError as err:
                    self.fail(str(err))

    def testStarParsingNASA():
            stars = buildDictStarExistingField(nas, "nasa")
            try:
                star = stars["sun"]
                mars = star.planetObjects["mars"]
                verifyPlanet(mars)
            except KeyError as err:
                self.fail(str(err))

    def verifyPlanet(planet):
        data = planet.getData()
        self.assertEqual(len(data), 7)
        self.assertEqual(data["mass"], 10)
        self.assertEqual(data["radius"], 3.14)
        self.assertEqual(data["period"],0.7)
        self.assertEqual(data["semimajoraxis"],.5)
        self.assertEqual(data["eccentricity"],1)
        self.assertEqual(data["discoverymethod"], "RV")
        self.assertEqual(data["discoveryyear"], 2001)
        self.assertEqual(data["lastupdate"],"5/16/2004")
        self.assertEqual(planet.name, "mars")