from testDiff import getDiff
import xml.etree.ElementTree as ET, urllib.request, gzip, io
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

class Planet:
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
        

def buildPlanetFromXML():
    for planet in oec.findall(".//planet"):
        planetBuilder = Planet.Builder("tempName")
        i = 0
        for child in planet.findall(".//name"):
            if child.tag == "name":
                if i == 0:
                    planetBuilder = Planet.Builder(child.text)
                elif i == 1:
                    planetBuilder.addValList("otherName", child.text)
                else:
                    planetBuilder.addToValList("otherName", child.text)
                i += 1
            else:
                planetBuilder.addToValList("otherName", child.text)
        planetBuilder.addVal("mass", planet.findtext("mass"))

        planet = planetBuilder.compile();

        '''
        for child in planet:
            planetBuilder = Planet.Builder(planet.findtext("name"))
            planetBuilder.addVal(child.tag, child.attrib)
        '''
        planet = planetBuilder.compile();
        print(planet);
    '''
    # Find all circumbinary planets
    for planet in oec.findall(".//binary/planet"):
        print(planet.findtext("name"))

    # Output distance to planetary system (in pc, if known) and number of planets in system
    for system in oec.findall(".//system"):
        print(system.findtext("distance"), len(system.findall(".//planet")))
    '''

buildPlanetFromXML()

def buildPlanet(line):
    _data_field = dict();
    _name = 0;
    _wanted = ["mass", "radius", "orbital_period"]
    for i in _wanted:
        temp = " ".join(i.split("_"));
        _data_field[temp] = heads.index(i);
    
    planetBuilder = Planet.Builder(line[_name]);
    
    for i in _data_field:
        planetBuilder.addVal(i, line[_data_field[i]]);
        
    planet = planetBuilder.compile();    
    return planet;
'''
file = open("exoplanet.eu_catalog-2.csv", "r")
lines = getDiff()
heads = file.readline().split(',')
print(heads)
line = file.readline()
while(line):
    line = line.split(',');
    print(buildPlanet(line));
    line = file.readline();
'''

buildPlanetFromXML()