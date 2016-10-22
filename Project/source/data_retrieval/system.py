# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 15:46:05 2016

@author: jerry
"""

import xml.etree.ElementTree as ET, urllib.request, gzip, io
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

class System:
    def __init__(self):
        self.data = dict();
    def __str__(self):
        out = "";
        for i in self.data:
            out += (i + ":");
            out += str(self.data[i]);
            out += " ";
        return out;
        
    class Builder:
        def __init__(self, name):
            self._data = {"name": name};
            
        def addVal(self, name, val):
            val = self._fixVal(val);
            self._data[name] = val;
            return self;

        def addValList(self, name, val):
            val = self._fixVal(val)
            self._data[name] = [val]
            return self

        def addToValList(self, name, val):
            val = self._fixVal(val)
            self._data[name] += [val]
            return self

        def compile(self):
            planet = Planet();
            planet.data = self._data;
            return planet;
        
        def _fixVal(self, val):
            temp = None;
            if(val != ''):
                try:
                    temp = float(val);
                except ValueError:
                    temp = val;
                except TypeError:
                    temp = "N/A";
            else:
                temp = "N/A";
            return temp;
            
def buildSystemFromXMLa():
    for system in oec.findall(".//system"):