from data_parsing.XML_data_parser import *
import unittest


class TestbuildSystemFromXML(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestbuildSystemFromXML, self).__init__(*args, **kwargs)
        (self.systems, self.stars, self.planets, self.allSystemsDict,
         self.allStarsDict,
         self.allPlanetsDict) = buildSystemFromXML("../storage/OEC_XML.gz")

    def test_planets_type(self):
        self.assertTrue(isinstance(self.planets, list),
                        "planets returned should be a list")

    def test_stars_type(self):
        self.assertTrue(isinstance(self.stars, list),
                        "stars returned should be a list")

    def test_systems_type(self):
        self.assertTrue(isinstance(self.systems, list),
                        "systems returned should be a list")

    def test_planet_fields(self):
        self.assertEquals(self.planets[0].name, "11 Com b",
                          "incorrect name")
        self.assertEquals(self.planets[0].data["period"], "326.03",
                          "incorrect period")
        self.assertEquals(self.planets[0].data["mass"], "19.4",
                          "incorrect mass")

    def test_star_fields(self):
        self.assertEquals(self.stars[0].name, "11 Com",
                          "incorrect name")
        self.assertEquals(self.stars[0].data["radius"], "19",
                          "incorrect radius")
        self.assertEquals(self.stars[0].data["temperature"], "4742",
                          "incorrect temperature")

    def test_system_fields(self):
        self.assertEquals(self.systems[0].name, "11 Com",
                          "incorrect name")
        self.assertEquals(self.systems[0].data["distance"], "88.9",
                          "incorrect distance")
        self.assertEquals(self.systems[0].data["declination"], "+17 47 34",
                          "incorrect declination")

    def test_number_of_planets(self):
        self.assertEquals(len(self.planets), 3397,
                          "incorrect number of planets")

    def test_number_of_stars(self):
        self.assertEquals(len(self.stars), 2658,
                          "incorrect number of stars")

    def test_number_of_systems(self):
        self.assertEquals(len(self.systems), 2500,
                          "incorrect number of systems")

    def test_alternate_names(self):
        planet = self.planets[0]
        self.assertEquals(planet.starObject,
                          planet.starObjectNamesToStar["11 Comae Berenices"])
        self.assertEquals(planet.starObject,
                          planet.starObjectNamesToStar["HD 107383"])
        self.assertEquals(planet.starObject,
                          planet.starObjectNamesToStar["HIP 60202"])
        self.assertEquals(planet.starObject,
                          planet.starObjectNamesToStar["TYC 1445-2560-1"])
        self.assertEquals(planet.starObject,
                          planet.starObjectNamesToStar["SAO 100053"])
        self.assertEquals(planet.starObject,
                          planet.starObjectNamesToStar["HR 4697"])
        self.assertEquals(planet.starObject,
                          planet.starObjectNamesToStar["BD+18 2592"])
        self.assertEquals(planet.starObject,
                          planet.starObjectNamesToStar[
                              "2MASS J12204305+1747341"])


if __name__ == "__main__":
    unittest.main(exit=False)
