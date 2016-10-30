from data_parsing.CSV_data_parser import *
from data_parsing.Planet import *
from data_parsing.PlanetaryObject import *
import unittest

class TestCSV_parser:
        exo = "exoplanetEU_csv"
        nas = "nasa_csv"
        def testFullPlanetParsingEU():
                planets = buildListPlanets(exo,["mass","radius","period","semimajoraxis","eccentricity",
                        "discoverymethod","discoveryyear","lastupdate"], exo)
                planet = planets[0]
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

        def testFullPlanetParsingNASA():
                pass

        def testStarParsingEU():
                pass

        def testStarParsingNASA():
                pass