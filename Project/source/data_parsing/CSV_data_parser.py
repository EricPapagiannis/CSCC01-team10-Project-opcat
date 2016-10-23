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
planets = dict()
while(line):
    line = line.split(',');
    planet = buildPlanet(line)
    palnets[planets._data["namePlanet"]] = planet
    line = file.readline();