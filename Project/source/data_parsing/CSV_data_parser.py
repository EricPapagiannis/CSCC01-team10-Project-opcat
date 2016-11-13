import sys
sys.path.append('../')
from data_parsing.Planet import Planet
from data_parsing.Star import Star
from csv import reader

# tags
eu = {"name":"name","mass": "mass", "radius":"radius", "period":"orbital_period", "semimajoraxis":"semi_major_axis",
    "eccentricity":"eccentricity", "discoverymethod":"detection_type", "discoveryyear":"discovered",
    "lastupdate":"updated", "nameStar":"star_name"}
nasa = {"name":"pl_hostname", "radius":"pl_radj", "eccentricity":"pl_orbeccen", "period":"pl_orbper",
    "lastupdate":"rowupdate", "discoverymethod":"pl_discmethod", "mass":"pl_bmassj","nameStar":"pl_hostname"}

eustar = {'rightascension':'ra', 'declination':'dec', 'distance':'star_distance', 'name':'star_name', 'mass':'star_mass', 'radius':'star_radius', 'magV':'mag_v', 'magB':'', 'magI':'mag_i', 'magJ':'mag_j', 'magH':'mag_h', 'magK':'mag_k', 'temperature':'star_teff', 'metallicity':'star_metallicity', 'spectraltype':'star_sp_type'}
nasastar = {'rightascension':'ra_str', 'declination':'dec_str', 'distance':'st_dist', 'name':'pl_hostname', 'mass':'st_mass', 'radius':'st_rad', 'magV':'st_optmag', 'magB':'', 'magJ':'', 'magH':'', 'magK':'', 'temperature':'st_teff', 'metallicity':'', 'spectraltype':''}


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
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        file = open("../storage/" + filename, "r")
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
        line = next(reader(line.splitlines()))
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
    '''(str, str)-> dict of stars
    Returns a dict of stars of planets built from the specific file
    '''
    stars = dict()
    if(source == "eu"):
        wanted = eu.keys()
    else:
        wanted = nasa.keys()
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        file = open("../storage/" + filename, "r")
    heads = file.readline().split(',')
    # removing new lines
    if(heads[-1][-1] == '\n'):
        heads[-1] = heads[-1][:-1]
    line = file.readline()
    while(line == '\n'):
        line = file.readline()

    while(line):
        line = next(reader(line.splitlines()))
        planet = buildPlanet(line, heads, wanted, source)
        star = buildStar(line, heads, source)
        stars[star.name] = star
        star.planetObjects += [planet]
        line = '\n'
        while(line == '\n'):
            line = file.readline()
    return stars

def buildStar(line, heads, source):
    '''(str, list of str, str) -> star
    Returns a star object from parsing the line
    '''
    _data_field = dict()
    if(source == 'eu'):
        _actual = eustar
    else:
        _actual = nasastar
    for i in _actual:
        try:
            _data_field[i] = heads.index(_actual[i])
        except ValueError:
            pass
    _name = line[_data_field['name']]

    star = Star(_name)
    for i in _data_field:
        try:
            star.addVal(i, _fixVal(i, line[_data_field[i]], source))
        except KeyError:
            planet.addVal(i, '')
    return star

def buildListStarAllField(filename, source):
    ''' (str, str) -> list star
    Idk why this is here since it has the exact same functionality as buildListStarExistingField
    but... it's here so yeah.
    '''
    return list(buildDictStarExistingField(filename, source).value())

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

        def convertEURA(data):
            deg = float(data)
            hour = deg / 15.0
            hours = int(hour)
            minute = (hour - float(hours))*60
            minutes = int(minute)
            second = (minute - float(minutes))*60
            re = str(hours) + ' ' + str(minutes) + ' ' + str(second)
            return re

        def convertNASARA(data):
            re = ''
            re += data[:2] + ' '
            re += data[3:5] + ' '
            re += data[6:-1]
            return re

        def convertNASADEC(data):
            re = ''
            re += data[:3] + ' '
            re += data[4:6] + ' '
            re += data[7:-1]
            return re

        def convertEUDEC(data):
            deg = float(data)
            hour = deg / 15.0
            hours = int(hour)
            minute = (hour - float(hours))*60
            minutes = int(minute)
            second = (minute - float(minutes))*60
            re = str(hours) + ' ' + str(minutes) + ' ' + str(second)
            return re

        # dict of functions for ea source's proper conversion
        eufunc = {'lastupdate':convertDate, 'rightascension':convertEURA, 'declination':convertEUDEC}
        nasafunc = {'lastupdate':convertDate, 'rightascension':convertNASARA, 'declination':convertNASADEC}
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