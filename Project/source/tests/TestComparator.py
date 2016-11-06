# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 20:20:42 2016

@author: jerry
"""

from data_comparison.Comparator import *
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
        self.assertRaises(ObjectTypeMismatchException, Comparator(self.planet1, self.Star1, "eu"))
        
    def testSQLjoin(self):
        comparator = Comparator(self.planet2, self.planet1, "eu")
        result = comparator.sqlJoin(True)
        self.assertEqual(result["data"], ["mass", "temperature"])
        self.assertEqual(result["left"], [12, 145])
        self.assertEqual(result["right"], [10, "N/A"])
        
    def testInnerJoinDiffFieldMatch(self):
        comparator = Comparator(self.Star1, self.Star2, "eu")
        inner = comparator.innerJoinDiff()
        self.assertEqual(inner, {})
        
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
        self.assertEqual(result["planetDN"], {str(self.planet1):{"data":["mass"], "left":[10], "right":[10]},
                         str(self.planet3):{"data":[], "left":[], "right":[]}})
        self.assertEqual(result["planetDC"], {str(self.planet1):{"mass": (10, 10)},str(self.planet3):{} })
        
if __name__ == "__main__":
    unittest.main(exit=False)