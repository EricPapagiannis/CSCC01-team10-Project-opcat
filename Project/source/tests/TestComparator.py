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
    planet1 = Planet("planet1")
    planet1.addVal("mass", 10)
    planet2 = Planet("planet2")
    planet2.addVal("mass", 12)
    planet2.addVal("temperature", 145)
    Star1 = Star("star1")
    Star1.addVal("mass", 100)
    Star2 = Star("star2")
    Star2.addVal("mass", 113)
    system1 = System("sys1")
    planet3 = Planet("planet3")
    planet4 = Planet("planet4")
    Star1.planetObjects = [planet1, planet3]
    Star2.planetObjects = [planet1, planet3, planet4]
    
    def __init__(self, *args, **kwargs):
        super(TestComparator, self).__init__(*args, **kwargs)

    def testRaiseTypeMismatch(self):
        try:        
            rip = Comparator(self.planet1, self.Star1, "eu")
        except ObjectTypeMismatchException:
            self.assertTrue(True)
        
    def testSQLjoin(self):
        comparator = Comparator(self.planet2, self.planet1, "eu")
        result = comparator.sqlJoin(True)
        try:
            self.assertEqual(result["data"], ["mass", "temperature"])
            self.assertEqual(result["left"], [12, 145])
            self.assertEqual(result["right"], [10, "N/A"])
        except:
            self.assertEqual(result["data"], ["temperature", "mass"])
            self.assertEqual(result["left"], [145, 12])
            self.assertEqual(result["right"], ["N/A", 10])
        
    def testInnerJoinDiffFieldMatch(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        inner = comparator.innerJoinDiff()
        self.assertEqual(inner, {'mass': (100.0, 113.0)})
        
    def testInnerJoinDiffFieldDiff(self):
        comparator = Comparator(self.planet1, self.planet2, "eu")
        inner = comparator.innerJoinDiff()
        self.assertEqual(inner, {"mass": (10, 12)})
        
    def testStarCompare(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        result = comparator.starCompare()
        self.assertEqual(result["starC"], {"mass": (100, 113)})
        self.assertEqual(result["starN"], {"data":["mass"], "left":[100], "right":[113]})
        self.assertEqual(result["planetN"], {"left":[], "right":[self.planet4]})
        self.assertEqual(result["planetDN"], {})
        self.assertEqual(result["planetDC"], {})
        self.assertEqual(result["planetA"], {"planet1":self.planet1, "planet3":self.planet3})
        
    def testproposedChangeStarCompare(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        result = comparator.proposedChangeStarCompare();
        answer = [self.planet1, self.planet3]
        self.assertEqual(len(result), len(answer))
        for i in range(0, len(result)-1):
            self.assertEqual(result[i].get_object_name(), answer[i].name)
        
if __name__ == "__main__":
    unittest.main(exit=False)