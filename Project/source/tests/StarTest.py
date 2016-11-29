# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 23:06:14 2016

@author: jerry
"""

from data_parsing.Star import *
from tests.PlanetaryObjectTest import *
import unittest


class TestStar(TestPlanetaryObject):
    def testInit(self):
        star1 = Star("testStar")
        self.assertEquals("testStar", star1.getName())
        self.assertEquals(None, star1.systemObject)
        self.assertEquals([], star1.planetObjects)
        self.assertEquals(dict(), star1.systemObjectNamesToSystem)
        self.assertEquals(dict(), star1.nameToPlanet)
        self.assertEquals(dict(), star1.errors)
        self.assertEquals([], star1.otherNamesStar)
        self.assertEquals([], star1.otherNamesSystem)
        self.assertEquals(dict(), star1.data)
        self.assertEquals("00/00/00", star1.lastupdate)


if __name__ == '__main__':
    unittest.main(exit=False)
