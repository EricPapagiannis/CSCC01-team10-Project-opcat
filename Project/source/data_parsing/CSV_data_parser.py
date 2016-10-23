from Planet import Planet
def buildPlanet(line, heads, wanted):
    _data_field = dict()
    _name = 0;
    _wanted = wanted
    for i in _wanted:
        temp = " ".join(i.split("_"))
        _data_field[temp] = heads.index(i)
    
    planet = Planet(line[_name])
    
    for i in _data_field:
        planet.addVal(i, line[_data_field[i]])

    return planet

def buildListPlanets(filename, wanted):
    file = open(filename, "r")
    heads = file.readline().split(',')
    line = file.readline()
    planets = dict()
    while(line):
        line = line.split(',')
        planet = buildPlanet(line, heads)
        planets[planet.data["namePlanet"]] = planet
        line = file.readline()
    return planets

if __name__ == "__main__":
    planets = buildListPlanets("exoplanet.eu_catalog-2.csv", ["mass", "radius", "orbital_period"])
    for i in planets:
        print(str(i))