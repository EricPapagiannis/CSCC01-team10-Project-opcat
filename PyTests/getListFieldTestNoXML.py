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
            self._data = {"name": name};
            
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

file = open("exoplanet.eu_catalog-2.csv", "r")
lines = getDiff()
heads = file.readline().split(',')
line = file.readline()
i = 1
while(line):
    if(i in lines):
        line = line.split(',');
        print(buildPlanet(line));
    line = file.readline();
    i += 1