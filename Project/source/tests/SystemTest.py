# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 23:01:56 2016

@author: jerry
"""

from data_parsing.System import *
from tests.PlanetaryObjectTest import *
import unittest


class TestSystem(TestPlanetaryObject):
    def testInit(self):
        system1 = System("testSystem")
        self.assertEquals("testSystem", system1.getName())
        self.assertEquals([], system1.starObjects)
        self.assertEquals(dict(), system1.errors)
        self.assertEquals([], system1.otherNamesSystem)
        self.assertEquals(dict(), system1.data)
        self.assertEquals("00/00/00", system1.lastupdate)


if __name__ == '__main__':
    unittest.main(exit=False)
