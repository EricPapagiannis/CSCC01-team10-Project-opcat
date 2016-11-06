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
        self.assertRaises(ObjectTypeMismatchException, Comparator(planet1, Star1))
        
    def testSQLjoin(self):
        comparator = Comparator(planet2, planet1)
        result = comparator.sqlJoin(True)
        self.assertEqual(result["data"], ["mass", "temperature"])
        self.assertEqual(result["left"], [12, 145])
        self.assertEqual(result["right"], [10, "N/A"])
        
    def testInnerJoinDiffFieldMatch(self):
        comparator = Comparator(Star1, Star2)
        inner = comparator.innerJoinDiff()
        self.assertEqual(inner, {})
        
    def testInnerJoinDiffFieldDiff(self):
        comparator = Comparator(planet1, planet2)
        inner = comparator.innerJoinDiff()
        self.assertEqual(inner, {"mass": (10, 12)})
        
    def testStarCompare(self):
        comparator = Comparator(Star1, Star2)
        result = comparator.starCompare()
        self.assertEqual(result["starC"], {"mass": (100, 113)})
        self.assertEqual(result["starN"], {"data":["mass"], "left":[100], "right":[113]})
        self.assertEqual(result["planetN"], {"left":[], "right":[planet4]})
        self.assertEqual(result["planetDN"], {str(planet1):{"data":["mass"], "left":[10], "right":[10]},
                         str(planet3):{"data":[], "left":[], "right":[]}})
        self.assertEqual(result["planetDC"], {str(planet1):{"mass": (10, 10)},str(planet3):{} })
        