# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 15:56:16 2016

@author: jerry
"""
import xml.etree.ElementTree as ET, urllib.request, gzip, io
from planetary_obj import planetary_obj
from system import System
#from system import system
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))
class Star(planetary_obj):
    def __init__(self):
        planetary_obj.init(self)
    def __str__(self):
        out = "";
        for i in self.data:
            out += (i + ":");
            out += str(self.data[i]);
            out += " ";
        return out;
            
def buildStarFromXML():
    for sys in oec.findall(".//system"):
        system = System.buildSystemFromXML(sys)
        print(system.getName())
        for star in sys.findall(".//star"):
            i = 0
            starBuilder = Star.Builder("tempName")
            for child in star.findall(".//name"):
            # used to build the namelist from openexoplanet
                if child.tag == "name":
                    if i == 0:
                        starBuilder = Star.Builder(child.text)
                    elif i == 1:
                        starBuilder.addValList("otherNames", child.text)
                    else:
                        starBuilder.addToValList("otherNames", child.text)
                    i += 1
                else:
                    starBuilder.addToValList("otherNames", child.text)
            starBuilder.addVal("mass", star.findtext("mass"));
            starBuilder.addVal("radius", star.findtext("radius"));
            starBuilder.addVal("temperature", star.findtext("temperature"));
            starBuilder.addVal("age", star.findtext("age"));
            starBuilder.addVal("metallicity", star.findtext("metallicity"));
            starBuilder.addVal("spectraltype", star.findtext("spectraltype"));
            starBuilder.addVal("magB", star.findtext("magB"));
            starBuilder.addVal("magV", star.findtext("magV"));
            starBuilder.addVal("magR", star.findtext("magR"));
            starBuilder.addVal("magI", star.findtext("magI"));
            starBuilder.addVal("magJ", star.findtext("magJ"));
            starBuilder.addVal("magH", star.findtext("magH"));
            starBuilder.addVal("magK", star.findtext("magK"));            
            starBuilder.addObj("system", system)
            star = starBuilder.compile()
            # example of getval with star subclass
            #print(star)
            
buildStarFromXML();