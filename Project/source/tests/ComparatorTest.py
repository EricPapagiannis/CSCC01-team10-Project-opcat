# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 20:20:42 2016

@author: jerry
"""
from data_comparison.Comparator import *
from data_comparison.proposed_change import *
from data_parsing.Planet import *
from data_parsing.PlanetaryObject import *
from data_parsing.Star import *
from data_parsing.System import *
import unittest


class TestComparator(unittest.TestCase):
    def setUp(self):
        self.planet1 = Planet("planet1")
        self.planet1.addVal("mass", 10)
        self.planet2 = Planet("planet2")
        self.planet2.addVal("mass", 12)
        self.planet2.addVal("temperature", 145)
        self.Star1 = Star("star1")
        self.Star1.addVal("mass", 100)
        self.Star2 = Star("star2")
        self.Star2.addVal("mass", 112)
        self.Star3 = Star("star3")

        self.system1 = System("sys1")
        self.planet3 = Planet("planet3")
        self.planet3.addVal("temperature", 145)
        self.planet4 = Planet("planet4")
        self.Star1.planetObjects = [self.planet1, self.planet3]
        self.Star2.planetObjects = [self.planet1, self.planet3, self.planet4]
        self.Star3.planetObjects = [self.planet1, self.planet3]

        self.EStar1 = Star("empty1")
        self.EStar2 = Star("empty2")

    def testCreateComparatorWithNonPlanetaryObjects(self):
        try:
            rip = Comparator("egg", 1, "eu")
        except ObjectTypeMismatchException:
            self.assertTrue(True)

    def testCreateComparatorWithDifferentPlanetaryObjects(self):
        try:
            rip = Comparator(self.planet1, self.Star1, "eu")
        except ObjectTypeMismatchException:
            self.assertTrue(True)

    def testSQLjoin(self):
        comparator = Comparator(self.planet2, self.planet1, "eu")
        result = comparator.sqlJoin(True)
        a = result["data"]
        b = ["mass", "temperature"]
        self.assertTrue(
            len(a) == len(b) and all(a.count(i) == b.count(i) for i in a))
        c = result["left"]
        d = [12, 145]
        self.assertTrue(
            len(c) == len(d) and all(c.count(i) == d.count(i) for i in c))
        e = result["right"]
        f = [10, "N/A"]
        self.assertTrue(
            len(e) == len(f) and all(e.count(i) == f.count(i) for i in e))

    def testInnerJoinDiffFieldMatch(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        inner = comparator.innerJoinDiff()
        self.assertEqual(inner, {'mass': (100, 112)})

    def testInnerJoinDiffFieldDiff(self):
        comparator = Comparator(self.planet1, self.planet3, "eu")
        inner = comparator.innerJoinDiff()
        self.assertEqual(inner, {})

    def testStarCompareWithNonStarObjects(self):
        comparator = Comparator(self.planet1, self.planet2, "eu")
        try:
            comparator.starCompare()
        except ObjectTypeIncompatibleException:
            self.assertTrue(True)

    def testStarCompareEmptyStarsStarC(self):
        comparator = Comparator(self.EStar1, self.EStar2, "eu")
        result = comparator.starCompare()
        self.assertEqual(result["starC"], {})

    def testStarCompareEmptyStarsStarN(self):
        comparator = Comparator(self.EStar1, self.EStar2, "eu")
        result = comparator.starCompare()
        self.assertEqual(result["starN"]["data"], [])
        self.assertEqual(result["starN"]["left"], [])
        self.assertEqual(result["starN"]["right"], [])

    def testStarCompareEmptyStarsPlanetN(self):
        comparator = Comparator(self.EStar1, self.EStar2, "eu")
        result = comparator.starCompare()
        self.assertEqual(result["planetN"]["left"], [])
        self.assertEqual(result["planetN"]["right"], [])

    def testStarCompareEmptyStarsPlanetDN(self):
        comparator = Comparator(self.EStar1, self.EStar2, "eu")
        result = comparator.starCompare()
        self.assertEqual(result["planetDN"], {})

    def testStarCompareEmptyStarsPlanetDC(self):
        comparator = Comparator(self.EStar1, self.EStar2, "eu")
        result = comparator.starCompare()
        self.assertEqual(result["planetDC"], {})

    def testStarCompareEmptyStarsPlanetA(self):
        comparator = Comparator(self.EStar1, self.EStar2, "eu")
        result = comparator.starCompare()
        self.assertEqual(result["planetA"], {})

    def testStarCompareStarWithOneFieldStarC(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        result = comparator.starCompare()
        starC = result["starC"]
        answer = {"mass": (100.0, 112.0)}
        self.assertEqual(starC, answer)

    def testStarCompareStarWithOneFieldStarN(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        result = comparator.starCompare()
        starN = result["starN"]
        answer = {"data": ["mass"], "left": [100.0], "right": [112.0]}
        self.assertEqual(starN, answer)

    def testStarCompareStarWithOneFieldStarN2(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        result = comparator.starCompare()
        planetN = result["planetN"]
        answer = {"left": [], "right": [self.planet4]}
        self.assertEqual(planetN, answer)

    def testStarCompareStarWithOneFieldPlanetDN(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        result = comparator.starCompare()
        planetDN = result["planetDN"]
        answer = {}
        self.assertEqual(planetDN, answer)

    def testStarCompareStarWithOneFieldPlanetDC(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        result = comparator.starCompare()
        planetDC = result["planetDC"]
        answer = {}
        self.assertEqual(planetDC, answer)

    def testStarCompareStarWithOneFieldPlanetA(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        result = comparator.starCompare()
        planetA = result["planetA"]
        answer = {"planet1": self.planet1, "planet3": self.planet3}
        self.assertEqual(planetA, answer)

    def testproposedChangeStarCompare(self):
        comparator = Comparator(self.Star3, self.Star2, "eu")
        result = comparator.proposedChangeStarCompare()
        resultNames = [result[0].get_object_name(), result[1].get_object_name()]
        answer = [self.planet1.name, self.planet3.name]
        print(resultNames, answer)
        self.assertTrue(
            len(resultNames) == len(answer) and all(
                resultNames.count(i) == answer.count(i) for i in resultNames))


if __name__ == "__main__":
    unittest.main(exit=False)
