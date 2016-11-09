import gzip
import io
import urllib.request
import xml.etree.ElementTree as ET

from data_parsing.System import *
from data_parsing.Star import *
from data_parsing.Planet import *

url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
'''
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))
'''


def downloadXML(path="../storage/OEC_XML.gz"):
    ''' 
    () -> ()
    Opens OEC.gz as a series of XML documents for reading. 
    '''
    # Write to file
    file = io.BytesIO(urllib.request.urlopen(url).read())
    with gzip.open(path, "wb") as f_out, gzip.open(file, 'rb') as f_in:
        f_out.writelines(f_in)
    f_out.close()
    f_in.close()


# Read from file
def readXML(path="../storage/OEC_XML.gz"):
    '''
    () -> ElementTree
    Parses OEC as an ElementTree
    '''
    with gzip.open(path, "rb") as f:
        oec = ET.parse(f)
    f.close()
    return oec


# returns a tuple of a (list of all system objects, list of star objects, list of all planet objects)
# system has reference to its stars
# stars has reference to its planets

# planets have reference to the star and system it is in
# stars have reference to the system it is in
def buildSystemFromXML(path="../storage/OEC_XML.gz"):
    '''
    () -> ([System], [Star], [Planet], {systemName: System}, {starName: Star},
           {planetName: Planet})
    Assuming a valid connection, parse the xml from the big xml document
    that contains every system into a tuple of system objects, star objects,
    and planet objects. Each Planetary Object dictionary contains the fields
    that are present from the xml it was parsed from, no more, no less.
    The system have a list of references to its stars, the stars have a list of
    references to its planets, and the planets have a reference to the star
    and system it is in, and stars have a refernece to the system it is in
    REQ: Valid internet connection
    '''
    # initialize empty lists that will be returned at the end  of all
    # planetary objects
    oec = readXML(path)
    allSystems = []
    allStars = []
    allPlanets = []
    allSystemsDict = dict()
    allStarsDict = dict()
    allPlanetsDict = dict()
    # loop through each system in the xml
    for systemXML in oec.findall(".//system"):
        # loop through teach tag in the system that is name
        i = 0
        for child in systemXML.findall(".//name"):
            if child.tag == "name":
                # if it is the first name, create a System object with that
                # main name
                if i == 0:
                    systemName = child.text
                    system = System(systemName)
                    allSystemsDict[child.text] = system
                # if there are more names, create / add them to other names list
                elif i == 1:
                    # system.addValList("otherNamesSystem", child.text)
                    system.otherNamesSystem.append(child.text)
                    allSystemsDict[child.text] = system
                else:
                    # system.addToValList("otherNamesSystem", child.text)
                    system.otherNamesSystem.append(child.text)
                    allSystemsDict[child.text] = system
                i += 1
            else:
                # system.addToValList("otherNamesSystem", child.text)
                system.otherNamesSystem.append(child.text)
                allSystemsDict[child.text] = system

        # build the system data dictionary mapping the tag name to the tag value
        # in the system
        for child in systemXML:
            if (child.tag.lower() != "star") and (child.tag.lower() != "name"):
                system.addVal(child.tag, child.text)

        # build a list of stars that are in the system
        stars = []
        # loop through each star in the system
        localStarsDict = dict()
        for starXML in systemXML.findall(".//star"):
            ii = 0
            # loop through teach tag in the star that is name
            for child in starXML.findall(".//name"):
                if child.tag == "name":
                    # if it is the first name, create a Star object with that
                    # main name
                    if ii == 0:
                        star = Star(child.text)
                        # system.addValList("stars", child.text)
                        allStarsDict[child.text] = star
                        localStarsDict[child.text] = star
                    # if there are more names, create / add them to other names
                    # list
                    elif ii == 1:
                        # star.addValList("otherNamesStar", child.text)
                        star.otherNamesStar.append(child.text)
                        allStarsDict[child.text] = star
                        localStarsDict[child.text] = star
                    else:
                        # star.addToValList("otherNamesStar", child.text)
                        star.otherNamesStar.append(child.text)
                        allStarsDict[child.text] = star
                        localStarsDict[child.text] = star
                    ii += 1
                else:
                    # star.addToValList("otherNamesStar", child.text)
                    star.otherNamesStar.append(child.text)
                    allStarsDict[child.text] = star
                    localStarsDict[child.text] = star

            # build the star data dictionary mapping the tag name to the tag
            # value in the system
            for child in starXML:
                if (child.tag.lower() != "planet") and (
                            child.tag.lower() != "name"):
                    star.addVal(child.tag, child.text)

            # build a list of planets that are in the star
            planets = []
            # loop through each planet in the star
            localPlanetsDict = dict()
            for planetXML in starXML.findall(".//planet"):
                iii = 0
                # loop through teach tag in the planet that is name
                for child in planetXML.findall(".//name"):
                    if child.tag == "name":
                        # if it is the first name, create a Planet object with
                        # that main name
                        if iii == 0:
                            planet = Planet(child.text)
                            # star.addValList("planets", child.text)
                            allPlanetsDict[child.text] = planet
                            localPlanetsDict[child.text] = planet
                        # if there are more names, create / add them to other
                        # names list
                        elif iii == 1:
                            # planet.addValList("otherNamesPlanet", child.text)
                            planet.otherNamesPlanet.append(child.text)
                            allPlanetsDict[child.text] = planet
                            localPlanetsDict[child.text] = planet
                        else:
                            # planet.addToValList("otherNamesPlanet", child.text)
                            planet.otherNamesPlanet.append(child.text)
                            allPlanetsDict[child.text] = planet
                            localPlanetsDict[child.text] = planet
                        iii += 1
                    else:
                        # planet.addToValList("otherNamesPlanet", child.text)
                        planet.otherNamesPlanet.append(child.text)
                        allPlanetsDict[child.text] = planet
                        localPlanetsDict[child.text] = planet

                # build the planet data dictionary mapping the tag name to the
                # tag value in the system
                for child in planetXML:
                    if (child.tag.lower() != "name"):
                        planet.addVal(child.tag, child.text)

                # add the star name that the planet is in
                # planet.addVal("nameStar", star.getVal("nameStar"))
                planet.nameStar = star.name
                # planet.starObjectNamesToStar[star.getVal("nameStar")] = star
                planet.starObjectNamesToStar[star.name] = star
                starData = star.getData()
                # and others if there are any
                '''
                if "otherNamesStar" in starData:
                    planet.addValList("otherNamesStar",
                                      starData["otherNamesStar"])
                    for starObject in starData["otherNamesStar"]:
                        planet.starObjectNamesToStar[
                            starObject] = star
                '''
                planet.otherNamesStar = star.otherNamesStar
                for starObject in star.otherNamesStar:
                    planet.starObjectNamesToStar[
                        starObject] = star
                # add this planet to the list of planets in the star
                planets.append(planet)
                # and all planets list
                allPlanets.append(planet)
                # add the star reference in the planet
                # planet.addVal("starObject", star)
                planet.starObject = star

                # print("PLANET: ", planet)

            # add the list of planets in the star to the star
            # star.addValList("planetObjects", planets)
            star.planetObjects = planets
            # add the name of the system that the star is in
            # star.addVal("nameSystem", system.getVal("nameSystem"))
            star.nameSystem = system.name
            # star.systemObjectNamesToSystem[star.getVal("nameSystem")] = system
            star.systemObjectNamesToSystem[star.nameSystem] = system
            star.nameToPlanet = localPlanetsDict
            systemData = system.getData()
            # and others if there are any
            '''
            if "otherNamesSystem" in systemData:
                star.addValList("otherNamesSystem",
                                systemData["otherNamesSystem"])
                for systemObject in systemData["otherNamesSystem"]:
                    star.systemObjectNamesToSystem[
                        systemObject] = system
            '''
            star.otherNamesSystem = system.otherNamesSystem
            for systemObject in system.otherNamesSystem:
                star.systemObjectNamesToSystem[
                    systemObject] = system
            # add the stars to the list of stars in the system
            stars.append(star)
            # and all stars list
            allStars.append(star)
            # add the system reference in the star
            # star.addVal("systemObject", system)
            star.systemObject = system
            # add the list of stars in the system to the system
            # system.addValList("starObjects", stars)
            system.starObjects = stars
            system.nameToStar = localStarsDict
            # print("STAR: ", star)
        # add the system to the list of all systems list
        allSystems.append(system)
        # print("SYSTEM: ", system)
        # print('\n\n')

    return (allSystems, allStars, allPlanets, allSystemsDict, allStarsDict,
            allPlanetsDict)


if __name__ == "__main__":
    '''
    (a, b, c, d, e, f) = buildSystemFromXML()
    print(b)
    print(len(b))
    print(e)
    print(len(e))
    '''

''' givin a proposed change which inlcudes:
the changes from the original planet
and a reference to the planet


algorithm outline:
loop through each proposed change (make into other method)
get the reference from the proposed change
figure out how to get xml from one planet on oec github givin the name of system (stored in planet)
then do stuff similar to download
ie. find the planet in the system
instead of storing the field, replace it with the new one from proposed change
finalize the field updating
pull request? with new xml string (maybe have to turn into file first, then delete after?) on the link
'''


def uploadProposedChange():
    pass
