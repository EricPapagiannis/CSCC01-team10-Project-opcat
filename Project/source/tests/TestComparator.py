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
    def __init__(self, *args, **kwargs):
        super(TestComparator, self).__init__(*args, **kwargs)