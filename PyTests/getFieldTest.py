from testDiff import getDiff

# ************ CHANGES MADE ***************

class Planet:
    def __init__(self):
        self.name = None;
        self.mass = None;
        self.radius = None;
        self.orbital_period = None;
        
    def __str__(self):
        return (str(self.name) + " " + str(self.mass) + " " + str(self.radius)
                + " " + str(self.orbital_period));
        
    class Builder:
        def __init__(self, name):
            self._name = name;
            self._mass = None;
            self._radius = None;
            self._orbitalPeriod = None;
            
        def mass(self, mass):
            if(mass != ''):
                self._mass = float(mass);
            return self;
        
        def radius(self, radius):
            if(radius != ''):
                self._radius = float(radius);
                print(True);
            return self;
        
        def orbitalPeriod(self, orbit):
            if(orbit != ''):
                self._orbitalPeriod = float(orbit);
            return self;
        
        def compile(self):
            planet = Planet();
            planet.name = self._name;
            planet.mass = self._mass;
            planet.radius = self._radius;
            planet.orbital_period = self._orbitalPeriod;
            return planet;
        

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
    .radius(line[_radius])\
    .mass(line[_mass])\
    .orbitalPeriod(line[_oP])\
    .compile()
print(planet)