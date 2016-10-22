# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 15:56:16 2016

@author: jerry
"""
import xml.etree.ElementTree as ET, urllib.request, gzip, io
from planetary_obj import planetary_obj
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
            
def buildStarFromXMLa():
    b = 1
    for system in oec.findall(".//system"):
        for star in system.findall(".//star"):
            i = 0
            starBuilder = Star.Builder("tempName")
            for child in star.findall(".//name"):
            # used to build the namelist from openexoplanet
                if child.tag == "name":
                    if i == 0:
                        starBuilder = Star.Builder(child.text)
                        print(child.text)
                    elif i == 1:
                        starBuilder.addValList("otherNames", child.text)
                    else:
                        starBuilder.addToValList("otherNames", child.text)
                    i += 1
                else:
                    starBuilder.addToValList("otherNames", child.text)
            star = starBuilder.compile()
            print(star)
            
buildStarFromXMLa();
        