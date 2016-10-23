# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 17:47:49 2016

@author: jerry
"""

import xml.etree.ElementTree as ET, urllib.request, gzip, io
from system import System
from Star import Star
from planet import Planet
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))
# builds dictionary catalogue from oec. 
def buildDatabase():
    catalogue = dict();
    # look through each system and build system object
    for system in oec.findall(".//system"):
        newsys = System.buildSystemFromXML(system);
        # look through each star in system and build star object, refrence it
        for star in system.findall(".//star"):
            newStar = Star.buildStarFromXML(star);
            newStar.addRefrence("System", newsys);
            newsys.addRefrence("Star", newStar)
            # vice versa with planets
            for planet in star.findall(".//planet"):
                newPlanet = Planet.buildPlanetFromXML(planet);
                newPlanet.addRefrence("System", newsys);
                newPlanet.addRefrence("Star", newStar);
                newsys.addRefrence("Planet", newPlanet)
                newStar.addRefrence("Planet", newPlanet);
                catalogue[newPlanet.getName()] = newPlanet;
    return catalogue
database = buildDatabase();
for i in database:
    print([database[i].getval("System").getName(), database[i].getName()]);