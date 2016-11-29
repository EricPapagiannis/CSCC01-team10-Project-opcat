# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 19:03:43 2016

@author: jerry
"""
from data_parsing.PlanetaryObject import *
import unittest


class TestPlanetaryObject(unittest.TestCase):
    def setUp(self):
        self.planet1 = PlanetaryObject()
        self.planet2 = PlanetaryObject("test")

    def testGetDataOnEmptyPlanet(self):
        actual = self.planet1.getData()
        expected = dict()
        self.assertEquals(expected, actual)

    def testInitWithString(self):
        actual = self.planet2.getData()
        expected = {"namePlanetaryObject": None, "test": None}
        self.assertEquals(expected, actual)

    def testInitWithNonString(self):
        set = ["test"]
        self.failUnlessRaises(TypeError, PlanetaryObject, set)

    def getGetNameOnNonNamedPlanet(self):
        expected = None
        self.assertEquals(expected, self.planet1.getName())

    def getNameNonEmptyOnNamedPlanet(self):
        self.assertEquals("test", self.planet2.getName())

    def testGetValOnMissingField(self):
        self.failUnlessRaises(KeyError, self.planet1.getVal, "name")
        self.failUnlessRaises(KeyError, self.planet2.getVal, "name")

    def testAddValOnEmptyPlanet(self):
        self.planet1.addVal("name", "string")
        self.assertEquals("string", self.planet1.getVal("name"))

    def testAddValOnNamedPlanet(self):
        self.planet2.addVal("name", "string")
        self.assertEquals("string", self.planet2.getVal("name"))

    def testAddMultipleVals(self):
        for i in range(1, 100):
            self.planet2.addVal(i, i)
            value = self.planet2.getVal(i)
            self.assertEquals(i, value)

    def testAddPlanetaryObjectAsVal(self):
        self.planet1.addVal("planet", self.planet2)
        expected = {"planet": self.planet2}
        self.assertEquals(self.planet2, self.planet1.getVal("planet"))
        self.assertEquals(expected, self.planet1.getData())

    def testAddValListString(self):
        self.planet1.addValList("test", "String")
        self.assertEquals(["String"], self.planet1.getVal("test"))

    def testAddValListInputList(self):
        self.planet1.addValList("test", ["String", 1, "planet", self.planet2])
        expected = ["String", 1, "planet", self.planet2]
        self.assertEquals(expected, self.planet1.getVal("test"))

    def testAddValListInt(self):
        self.planet2.addValList("test", 2)
        expected = [2.0]
        self.assertEquals(expected, self.planet2.getVal("test"))

    def testAddValListNonCompatibleObject(self):
        self.planet2.addValList("test", self.planet1)
        expected = ["N/A"]
        self.assertEquals(expected, self.planet2.getVal("test"))

    def testAddToValListExistingList(self):
        self.planet2.addValList("test", 2)
        self.planet2.addToValList("test", 3)
        expected = [2, 3]
        self.assertEquals(expected, self.planet2.getVal("test"))

    def testAddToValListNoExistingKey(self):
        self.failUnlessRaises(TypeError, self.planet2.addToValList, "test", 3)

    def testAddToValListNonListAtKey(self):
        self.planet2.addVal("test", 3)
        self.failUnlessRaises(TypeError, self.planet2.addToValList, "test", 3)


if __name__ == "__main__":
    unittest.main(exit=False)
