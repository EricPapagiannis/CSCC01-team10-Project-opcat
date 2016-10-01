from testDiff import getDiff

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
            self._data = dict();
            
        def addVal(self, name, val):
            val = self._fixVal(val);
            self._data[name] = val;
            return self;
        
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
            else:
                temp = "N/A";
            return temp;
        

file = open("exoplanet.eu_catalog-2.csv", "r")
lines = getDiff()
heads = file.readline().split(',')
print(heads)
_name = 0
_mass = 1
_radius = heads.index("radius")
_oP = heads.index("orbital_period")
line = file.readline().split(',')
print(line)
print(_name, _mass, _radius, _oP)
print(line[_radius], line[_mass], line[_oP])
planet = Planet.Builder(line[_name])\
    .addVal("radius", line[_radius])\
    .addVal("mass", line[_mass])\
    .addVal("Orbital Period", line[_oP])\
    .compile()
print(planet)