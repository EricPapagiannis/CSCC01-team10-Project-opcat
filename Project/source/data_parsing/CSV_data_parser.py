from Planet import Planet

eu = {"mass": "mass", "radius", "orbital_period": "period", "semi_major_axis":"semimajoraxis",
    "eccentricity":"eccentricity", "detection_type":"discoverymethod"}
nasa = {}

correction = {"discoverymethod":discoveryCorrection}
discoveryCorrection = {"Radial Velocity": "RV", "Primary Transit": "transit", "Imaging":"imaging",
    "Pulsar":"timing", "Microlensing":"microlensing", "TTV":"transit", "Astrometry":"RV"}

def buildPlanet(line, heads, wanted, source):
    _data_field = dict()
    _name = 0
    _wanted = wanted

    if(source == "eu"):
        _actual = eu
    else (source == "nasa"):
        _actual = nasa

    for i in _wanted:
        temp = _actual[i]
        tempval = _fixval(heads.index(i))
        #if(heads.index(i) == "Other"):
        _data_field[temp] = tempval

    planet = Planet(line[_name])

    for i in _data_field:
        planet.addVal(i, line[_data_field[i]])

    return planet

def _fixVal(field, value):
    if(field in correction and value in correction[field]):
        return correction[field[value]]
    else:
        return value

def buildDictionaryPlanets(filename, wanted, source):
    file = open(filename, "r")
    heads = file.readline().split(',')
    line = file.readline()
    planets = dict()

    while(line):
        line = line.split(',')
        planet = buildPlanet(line, heads, source)
        planets[planet.data["namePlanet"]] = planet
        line = file.readline()
    return planets

def buildListPlanets(filename, wanted, source):
    tdict = buildDictionaryPlanets(filename, wanted)
    rlist = []

    for name in tdict:
        rlist += tdict[name]
    return rlist

if __name__ == "__main__":
    planets = buildListPlanets("exoplanet.eu_catalog-2.csv", ["mass", "radius", "orbital_period", 
        "semi_major_axis"], "eu")
    for i in planets:
        print(str(i))