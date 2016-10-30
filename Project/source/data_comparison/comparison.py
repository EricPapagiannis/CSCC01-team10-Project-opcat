# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 11:54:15 2016

@author: jerry
"""
from proposed_change import *
from data_parsing.planetary_object import *
from data_parsing.Planet import *
from data_parsing.Star import *
from data_parsing.System import *

star = Star("star1")
planet1 = Planet("planet1")
planet2 = Planet("planet2")
system1 = System("system")
star2 = Star("star2")

class Comparison:
    '''accepts an addition object or modification object'''