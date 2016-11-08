from data_parsing.Planet import Planet
from data_parsing.Star import Star
#from Planet import Planet
#from Star import star

eu = {"name":"# name","mass": "mass", "radius":"radius", "period":"orbital_period", "semimajoraxis":"semi_major_axis",
    "eccentricity":"eccentricity", "discoverymethod":"detection_type", "discoveryyear":"discovered",
    "lastupdate":"updated", "nameStar":"star_name"}
nasa = {"name":"pl_hostname", "radius":"pl_radj", "eccentricity":"pl_orbeccen", "period":"pl_orbper",
    "lastupdate":"rowupdate", "discoverymethod":"pl_discmethod", "mass":"pl_bmassj","nameStar":"pl_hostname"}

discoveryCorrection = {"Radial Velocity": "RV", "Primary Transit": "transit", "Imaging":"imaging",
    "Pulsar":"timing", "Microlensing":"microlensing", "TTV":"transit", "Transit Timing Variation":"transit",
    "Astrometry":"RV", "nameStar":"pl_hostname"}

correction = {"discoverymethod":discoveryCorrection}

def buildPlanet(line, heads, wanted, source):
    _name_index = 0
    _data_field = dict()

    if (source == "eu"):
        _actual = eu
    else:
        _actual = nasa

    for i in wanted:
        try:
            temp = _actual[i]
            tempval = heads.index(temp)
            _data_field[i] = tempval
        except ValueError:
            pass

    _name = line[_name_index]
    if(source == "nasa"):
        _name += (" " + line[_name_index+1])
    planet = Planet(_name)

    for i in _data_field:
        try:
            planet.addVal(i, _fixVal(i, line[_data_field[i]], source))
        except KeyError:
            planet.addVal(i,"")
    return planet

def _fixVal(field, value, source):
    re = value
    if(field in correction and value in correction[field].keys()):
        re = correction[field][value]
    try:
        res = float(re)
    except:
        res = re
    res = UnitConverter.convertToOpen(field, res, source)
    return res
    #return re

def buildDictionaryPlanets(filename, wanted, source):
    file = open(filename, "r")
    heads = file.readline().split(',')
    if(heads[-1][-1] == '\n'):
        heads[-1] = heads[-1][:-1]
    line = file.readline()
    while(line == "\n"):
        line = file.readline()
    planets = dict()

    while(line):
        line = line.split(',')
        planet = buildPlanet(line, heads, wanted, source)
        # planets[planet.data["namePlanet"]] = planet
        planets[planet.name] = planet
        line = '\n'
        while(line == '\n'):
            line = file.readline().rstrip().lstrip()
    file.close()
    return planets

def buildListPlanets(filename, wanted, source):
    tdict = buildDictionaryPlanets(filename, wanted, source)
    rlist = []

    for name in tdict:
        rlist += [tdict[name]]
    return rlist

def buildListPlanetsAllField(filename, source):
    if(source == eu):
        heads = eu.keys()
    else:
        heads = nasa.keys()
    return buildListPlanets(filename, heads, source)

def buildDictStar(planets, source):
    stars = dict()
    for planet in planets:
        starname = planet.getVal('nameStar')
        if starname not in stars:
            stars[starname] = Star(starname)
            stars[starname].planetObjects = [planet]
            # stars[starname].addValList("planetObjects", [planet])
        else:
            # stars[starname].addToValList("planetObjects", [planet])
            stars[starname].planetObjects.append(planet)
    return stars

def buildDictStarExistingField(filename, source):
    if(source == "eu"):
        wanted = eu.keys()
    else:
        wanted = nasa.keys()
    return buildDictStar(buildListPlanets(filename, wanted, source), source)

def buildListStar(filename, wanted, source):
    planets = buildListPlanets(filename, wanted, source)
    return buildDictStar.values()

def buildListStarExistingField(filename, source):
    if(source == "eu"):
        return  buildListStar(filename, eu, source)
    else: #source == "nasa"
        return buildListStar(filename, nasa, source)

def buildListStarAllField(filename, source):
    planets = buildListPlanetsAllField(filename, source)
    return buildDictStar.values()

class UnitConverter:
    def convertToOpen(field, data, source):
        def convertDate(data):
            data = data.split('-')
            if(len(data) != 3):
                return ''
            re = ''
            re += data[0][2:] + '/'
            re += data[1] + '/'
            re += data[2]
            return re

        eufunc = {'lastupdate':convertDate}
        nasafunc = {'lastupdate':convertDate}
        if source == "eu":
            if field not in eufunc.keys():
                return data
            result = eufunc[field](data)
        else:
            if field not in nasafunc.keys():
                return data
            result = nasafunc[field](data)
        return result


if __name__ == "__main__":
    planets = buildListPlanets("exoplanetEU_csv",
        ["mass", "radius", "period", "semimajoraxis", "discoveryyear", "lastupdate",
        "discoverymethod", "eccentricity"], "eu")
    for i in planets:
        print(str(i))
    print("<<<<<EU\n\n\n\n\n\nNASA>>>>>>")
    planets = buildListPlanets("nasa_csv", ["mass", "radius", "eccentricity", "period",
        "lastupdate", "discoverymethod"], "nasa")
    print(len(planets))
    for i in planets:
        print(str(i))