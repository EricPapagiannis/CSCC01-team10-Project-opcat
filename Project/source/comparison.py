# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 11:54:15 2016

@author: jerry
"""
from data_parsing.System import *
from data_parsing.Star import *
from data_parsing.Planet import *
from proposed_change import Addition
from proposed_change import Modification
star = Star("star1")
planet1 = Planet("planet1")
planet2 = Planet("planet2")
system1 = System("system")
star2 = Star("star2")
star3 = Star("star3")

star.planetObjects.append(planet1)
star2.planetObjects.append(planet2)
planet1.starObjects = star
planet2.starObjects = star2
catalogue_1 = {"star": star, "star3": star3}
catalogue_2 = dict()
catalogue_2["star2"] = star2

class Comparison:
    '''accepts an addition object or modification object'''
    def __init__(self, target, target_og, destination):
        # takes in a target dictionary, a string containing target database
        # origin, and the destination dictionary. All dictionaries contain a list of star objects
        self.target = target
        self.origin = target_og
        self.destination = destination
        self.changes = {"Additions":[], "Modifications":[]}
    
    def find_new_star(self):
        # for each key in target catalogue check if that key is also in the destination catalogue.
        new_star_list = []
        for star in self.target:
            if star not in self.destination:
                # create an addition object for each star not in the destination database
                new_star = Addition(self.origin, self.target[star]);
                new_star_list.append(new_star);
        self.changes["Additions"] = self.changes["Additions"] + new_star_list
        
    def find_new_planet(self):
        new_planet_list = []
        # for each star in the target database, check for any  planet additions
        for star in self.target:
            planet_list = self.target[star].planetObjects
            for planet in planet_list:
                planet_in = False
                for dest_star in self.destination:
                    if planet in dest_star.planetObjects:
                        planet_in = True
                if not planet_in:
                    new_planet = Addition(self.origin, planet)
                    new_planet_list.append(new_planet)
    def find_Mod_Star(self):
        pass
    def total_changes(self):
        return len(self.changes["Additions"]) + len(self.changes["Modifications"])

compare = Comparison(catalogue_1, "catalogue_1", catalogue_2)
compare.find_new_star()
for addition in compare.changes["Additions"]:
    print(addition)
