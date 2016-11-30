# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 22:51:21 2016

@author: jerry
"""

from data_parsing.Planet import *
from tests.PlanetaryObjectTest import *
import unittest


class TestPlanet(TestPlanetaryObject):
    def testInit(self):
        planet1 = Planet("testPlanet")
        self.assertEquals("testPlanet", planet1.getName())
        self.assertEquals(None, planet1.starObject)
        self.assertEquals(dict(), planet1.starObjectNamesToStar)
        self.assertEquals(dict(), planet1.errors)
        self.assertEquals([], planet1.otherNamesPlanet)
        self.assertEquals(dict(), planet1.data)
        self.assertEquals("", planet1.nameStar)
        self.assertEquals("00/00/00", planet1.lastupdate)


if __name__ == '__main__':
    unittest.main(exit=False)
