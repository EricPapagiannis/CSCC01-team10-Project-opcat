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
        self.assertEquals(self.planets[0].data["mass"], "19.4", "incorrect mass")

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
    def test_alternate_names_point_right_allSystemsDict(self):
        for sys in self.allSystemsDict:
            system = self.allSystemsDict[sys]
            for sysName in system.otherNamesSystem:
                self.assertEqual(self.allSystemsDict[sysName].name, 
                                 system.name)
    def test_alternate_names_point_right_allStarsDict(self):
        for sta in self.allStarsDict:
            star = self.allStarsDict[sta]
            for starName in star.otherNamesStar:
                self.assertEqual(self.allStarsDict[starName].name,
                                 star.name)
    def test_alternate_names_point_right_allPlanetsDict(self):
        for pla in self.allPlanetsDict:
            planet = self.allPlanetsDict[pla]
            for plaName in planet.otherNamesPlanet:
                self.assertEqual(self.allPlanetsDict[plaName].name,
                                 planet.name)

if __name__ == "__main__":
    unittest.main(exit=False)