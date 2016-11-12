from data_parsing.Planet import Planet
from data_parsing.Star import Star

# tags
eu = {"name":"name","mass": "mass", "radius":"radius", "period":"orbital_period", "semimajoraxis":"semi_major_axis",
    "eccentricity":"eccentricity", "discoverymethod":"detection_type", "discoveryyear":"discovered",
    "lastupdate":"updated", "nameStar":"star_name"}
nasa = {"name":"pl_hostname", "radius":"pl_radj", "eccentricity":"pl_orbeccen", "period":"pl_orbper",
    "lastupdate":"rowupdate", "discoverymethod":"pl_discmethod", "mass":"pl_bmassj","nameStar":"pl_hostname"}

# discovery method correction to xml
discoveryCorrection = {"Radial Velocity": "RV", "Primary Transit": "transit", "Imaging":"imaging",
    "Pulsar":"timing", "Microlensing":"microlensing", "TTV":"transit", "Transit Timing Variation":"transit",
    "Astrometry":"RV", "nameStar":"pl_hostname"}

# fields to correct
correction = {"discoverymethod":discoveryCorrection}

def buildPlanet(line, heads, wanted, source):
    ''' (list str, list str, list str, str) -> Planet
    Takes in the line read as a list, the titles of the file, the wanted field and parses the wanted field
    from the read line into a planet.
    '''
    _name_index = 0
    _data_field = dict()

    # putting correct source dict
    if (source == "eu"):
        _actual = eu
    else:
        _actual = nasa
    # get the field index in head
    for i in wanted:
        try:
            temp = _actual[i]
            tempval = heads.index(temp)
            # the dict saves the indii
            _data_field[i] = tempval
        except ValueError: # not parsing fields we can't find
            pass

    # name of planet is always first field
    _name = line[_name_index]
    # nasa is weird, it's first 2 field
    if(source == "nasa"):
        _name += (" " + line[_name_index+1])
    planet = Planet(_name)
    for i in _data_field:
        try:
            # we get the indexed field from line, fix the value and add it to planet
            planet.addVal(i, _fixVal(i, line[_data_field[i]], source))
        # if the field DNE then we add empty to it
        except KeyError:
            planet.addVal(i,"")
    return planet

def _fixVal(field, value, source):
    ''' (str, str, str) -> str
    Returns an appropriate str for the field (including unit conversion)
    '''
    re = value
    # if it's a field that needs to be corrected
    # this if will be converted to unit conversion as well
    if(field in correction and value in correction[field].keys()):
        re = correction[field][value]
    # don't need fixing val
    else:
        re = value
    # converting unit before returning
    return UnitConverter.convertToOpen(field, re, source)
    #return re

def buildDictionaryPlanets(filename, wanted, source):
    ''' (str, list str, str) -> dict of Planets
    Builds a dictionary of planets where name of planet is key to planets
    '''
    file = open(filename, "r")
    heads = file.readline().split(',')
    # remove the stupid new line
    if(heads[-1][-1] == '\n'):
        heads[-1] = heads[-1][:-1]
    line = file.readline()
    # python 3.4 is stupid and likes to randomly read just a new line char
    while(line == "\n"):
        line = file.readline()
    planets = dict()

    while(line):
        line = line.split(',')
        planet = buildPlanet(line, heads, wanted, source)
        planets[planet.name] = planet
        # might as well take advantage of the retardation
        line = '\n'
        while(line == '\n'):
            line = file.readline().rstrip().lstrip()
    file.close()
    return planets

def buildListPlanets(filename, wanted, source):
    ''' (str, list str, str) -> list of planets
    Build a list of planets
    '''
    # build dict then just add to list
    tdict = buildDictionaryPlanets(filename, wanted, source)
    rlist = []

    for name in tdict:
        rlist += [tdict[name]]
    return rlist

def buildListPlanetsAllField(filename, source):
    ''' (str, str) -> list of planets
    build a list of planets of all fields that are defined and parsable
    '''
    if(source == "eu"):
        heads = eu.keys()
    else:
        heads = nasa.keys()
    return buildListPlanets(filename, heads, source)

def buildDictStar(planets, source):
    ''' (list of planets, str) -> dict of stars
    Builds a dict of stars from a list of planets with the name of star as the key
    '''
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
    ''' (str, str) -> Dict of stars
    Builds dict of star with name of star as key for all fields that are parsable
    '''
    if(source == "eu"):
        wanted = eu.keys()
    else:
        wanted = nasa.keys()
    return buildDictStar(buildListPlanets(filename, wanted, source), source)

def buildListStar(filename, wanted, source):
    ''' (str, list str, str) -> list star
    Builds list of stars for the desired fields
    '''
    planets = buildListPlanets(filename, wanted, source)
    return buildDictStar(planets, source).values()

def buildListStarExistingField(filename, source):
    ''' (str, str) -> list star
    Builds a list of stars for all fields that are parsable
    '''
    if(source == "eu"):
        return  buildListStar(filename, eu, source)
    else: #source == "nasa"
        return buildListStar(filename, nasa, source)

def buildListStarAllField(filename, source):
    ''' (str, str) -> list star
    Idk why this is here since it has the exact same functionality as buildListStarExistingField
    but... it's here so yeah.
    '''
    planets = buildListPlanetsAllField(filename, source)
    return buildDictStar(planets, source).values()

class UnitConverter:
    ''' A class for converting units in NASA and EU to OEC's units
    '''
    def convertToOpen(field, data, source):
        ''' (str, obj, str) -> obj
        Literally the mother of all functions in this class, call it to convert anything.
        ANYTHING. Returns appropriate converted stuff
        '''
        def convertDate(data):
            ''' (str) -> str
            Converts the date to the format of OEC
            '''
            data = data.split('-')
            if(len(data) != 3):
                return ''
            re = ''
            re += data[0][2:] + '/'
            re += data[1] + '/'
            re += data[2]
            return re

        # dict of functions for ea source's proper conversion
        eufunc = {'lastupdate':convertDate}
        nasafunc = {'lastupdate':convertDate}
        if source == "eu":
            # don't need to convert
            if field not in eufunc.keys():
                return data
            # call dat function
            result = eufunc[field](data)
        else:
            # don't need to ocnvert
            if field not in nasafunc.keys():
                return data
            # call dat function doe
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