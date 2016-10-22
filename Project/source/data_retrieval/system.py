# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 15:46:05 2016

@author: jerry
"""

import xml.etree.ElementTree as ET, urllib.request, gzip, io
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))
from planetary_obj import planetary_obj
class System(planetary_obj):
    def __init__(self):
        planetary_obj.init(self)
    def __str__(self):
        out = "";
        for i in self.data:
            out += (i + ":");
            out += str(self.data[i]);
            out += " ";
        return out;
            
    def buildSystemFromXML(system):
        i = 0
        systemBuilder = System.Builder("tempName")
        for child in system.findall(".//name"):
        # used to build the namelist from openexoplanet
            if child.tag == "name":
                if i == 0:
                    systemBuilder = System.Builder(child.text)
                elif i == 1:
                    systemBuilder.addValList("otherNames", child.text)
                else:
                    systemBuilder.addToValList("otherNames", child.text)
                i += 1
            else:
                systemBuilder.addToValList("otherNames", child.text)
        systemBuilder.addVal("epoch", system.findtext("epoch"));
        systemBuilder.addVal("rightascension", system.findtext("rightascension"));
        systemBuilder.addVal("declination", system.findtext("declination"));
        systemBuilder.addVal("distance", system.findtext("distance"));
        return systemBuilder.compile()
        