from data_parsing.Planet import Planet
#from Planet import Planet

eu = {"mass": "mass", "radius":"radius", "period":"orbital_period", "semimajoraxis":"semi_major_axis",
    "eccentricity":"eccentricity", "discoverymethod":"detection_type", "discoveryyear":"discovered",
    "lastupdate":"updated"}
nasa = {"name":"pl_hostname", "radius":"pl_radj", "eccentricity":"pl_orbeccen", "period":"pl_orbper",
    "lastupdate":"rowupdate", "discoverymethod":"pl_discmethod", "mass":"pl_bmassj"}

discoveryCorrection = {"Radial Velocity": "RV", "Primary Transit": "transit", "Imaging":"imaging",
    "Pulsar":"timing", "Microlensing":"microlensing", "TTV":"transit", "Transit Timing Variation":"transit",
    "Astrometry":"RV"}

correction = {"discoverymethod":discoveryCorrection}

def buildPlanet(line, heads, wanted, source):
    _data_field = dict()
    _name_index = 0
    _wanted = wanted

    if(source == "eu"):
        _actual = eu
    else: #(source == "nasa")
        _actual = nasa

    for i in _wanted:
        try:
            temp = _actual[i]
            tempval = _fixVal(i, heads.index(temp))
        except KeyError:
            temp = i
        #if(heads.index(i) == "Other"):
        _data_field[i] = tempval

    # fixing nasa's weird naming thing
    _name = line[_name_index]
    if(source == "nasa"):
        _name += (" " + line[_name_index+1])
    #create planet
    planet = Planet(_name)

    for i in _data_field:
        try:
            planet.addVal(i, line[_data_field[i]])
        except KeyError:
            planet.addVal(i, "")

    return planet

def _fixVal(field, value):
    if(field in correction and value in correction[field]):
        return correction[field[value]]
    else:
        return value

def buildDictionaryPlanets(filename, wanted, source):
    file = open(filename, "r")
    heads = file.readline().split(',')
    if(heads[-1][-1] == '\n'):
        heads[-1] = heads[-1][:-1]
    line = file.readline()
    planets = dict()

    while(line):
        line = line.split(',')
        planet = buildPlanet(line, heads, wanted, source)
        planets[planet.data["namePlanet"]] = planet
        line = file.readline()
    file.close()
    return planets

def buildListPlanets(filename, wanted, source):
    tdict = buildDictionaryPlanets(filename, wanted, source)
    rlist = []

    for name in tdict:
        rlist += [tdict[name]]
    return rlist

def buildListPlanetsAllField(filename, source):
    file = open(filename, "r")
    heads = file.readline().split(',')
    file.close()
    return buildListPlanets(filename, heads, source)

if __name__ == "__main__":
    #try:
    planets = buildListPlanets("exoplanetEU_csv",
        ["mass", "radius", "period", "semimajoraxis", "discoveryyear", "lastupdate",
        "discoverymethod", "eccentricity"], "eu")
    for i in planets:
        print(str(i))
    print("<<<<<EU\n\n\n\n\n\nNASA>>>>>>")
    planets = buildListPlanets("nasa_csv", ["mass", "radius", "eccentricity", "period", 
        "lastupdate"], "nasa")#, "discoverymethod"], "nasa")
    print(len(planets))
    for i in planets:
        print(str(i))
            #pass
    #except:
        #print("what")
        pass
