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
    Assuming a valid connection, opens OEC.gz as a series of XML documents for
    reading.
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


def buildSystemFromXML(path="../storage/OEC_XML.gz"):
    '''
    () -> ([System], [Star], [Planet], {systemName: System}, {starName: Star},
           {planetName: Planet})
    Parse the xml from the big xml document
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
            cleanNameSystem = ''.join(
                ch for ch in child.text if ch.isalnum()).lower()
            if child.tag == "name":
                # if it is the first name, create a System object with that
                # main name
                if i == 0:
                    systemName = child.text
                    system = System(systemName)
                    allSystemsDict[child.text] = system
                    system.otherNamesSystem.append(cleanNameSystem)
                # if there are more names, create / add them to other names list
                elif i == 1:
                    system.otherNamesSystem.append(child.text)
                    system.otherNamesSystem.append(cleanNameSystem)
                    allSystemsDict[child.text] = system
                else:
                    system.otherNamesSystem.append(child.text)
                    system.otherNamesSystem.append(cleanNameSystem)
                    allSystemsDict[child.text] = system
                i += 1
            else:
                system.otherNamesSystem.append(child.text)
                system.otherNamesSystem.append(cleanNameSystem)
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
                cleanNameStar = ''.join(
                    ch for ch in child.text if ch.isalnum()).lower()
                if child.tag == "name":
                    # if it is the first name, create a Star object with that
                    # main name
                    if ii == 0:
                        star = Star(child.text)
                        allStarsDict[child.text] = star
                        localStarsDict[child.text] = star
                        localStarsDict[cleanNameStar] = star
                        star.otherNamesStar.append(cleanNameStar)
                    # if there are more names, create / add them to other names
                    # list
                    elif ii == 1:
                        star.otherNamesStar.append(child.text)
                        star.otherNamesStar.append(cleanNameStar)
                        allStarsDict[child.text] = star
                        localStarsDict[child.text] = star
                        localStarsDict[cleanNameStar] = star
                    else:
                        star.otherNamesStar.append(child.text)
                        star.otherNamesStar.append(cleanNameStar)
                        allStarsDict[child.text] = star
                        localStarsDict[child.text] = star
                        localStarsDict[cleanNameStar] = star
                    ii += 1
                else:
                    star.otherNamesStar.append(child.text)
                    star.otherNamesStar.append(cleanNameStar)
                    allStarsDict[child.text] = star
                    localStarsDict[child.text] = star
                    localStarsDict[cleanNameStar] = star

            # build the star data dictionary mapping the tag name to the tag
            # value in the system
            for child in starXML:
                if (child.tag.lower() != "planet") and (
                            child.tag.lower() != "name"):
                    star.addVal(child.tag, child.text)
                    for attribute in child.attrib:
                        if "error" in attribute or "limit" in attribute:
                            star.errors[child.tag + attribute] = child.attrib[
                                attribute]

            # build a list of planets that are in the star
            planets = []
            # loop through each planet in the star
            localPlanetsDict = dict()
            for planetXML in starXML.findall(".//planet"):
                iii = 0
                # loop through teach tag in the planet that is name
                for child in planetXML.findall(".//name"):
                    cleanNamePlanets = ''.join(
                        ch for ch in child.text if ch.isalnum()).lower()
                    if child.tag == "name":
                        # if it is the first name, create a Planet object with
                        # that main name
                        if iii == 0:
                            planet = Planet(child.text)
                            allPlanetsDict[child.text] = planet
                            localPlanetsDict[child.text] = planet
                            localPlanetsDict[cleanNamePlanets] = planet
                            planet.otherNamesPlanet.append(cleanNamePlanets)
                        # if there are more names, create / add them to other
                        # names list
                        elif iii == 1:
                            planet.otherNamesPlanet.append(child.text)
                            planet.otherNamesPlanet.append(cleanNamePlanets)
                            allPlanetsDict[child.text] = planet
                            localPlanetsDict[child.text] = planet
                            localPlanetsDict[cleanNamePlanets] = planet
                        else:
                            planet.otherNamesPlanet.append(child.text)
                            planet.otherNamesPlanet.append(cleanNamePlanets)
                            allPlanetsDict[child.text] = planet
                            localPlanetsDict[child.text] = planet
                            localPlanetsDict[cleanNamePlanets] = planet
                        iii += 1
                    else:
                        planet.otherNamesPlanet.append(child.text)
                        planet.otherNamesPlanet.append(cleanNamePlanets)
                        allPlanetsDict[child.text] = planet
                        localPlanetsDict[child.text] = planet
                        localPlanetsDict[cleanNamePlanets] = planet

                # build the planet data dictionary mapping the tag name to the
                # tag value in the system
                for child in planetXML:
                    if (child.tag.lower() != "name") and (
                                child.tag.lower() != "lastupdate"):
                        planet.addVal(child.tag, child.text)
                        for attribute in child.attrib:
                            if "error" in attribute or "limit" in attribute:
                                planet.errors[child.tag + attribute] = \
                                    child.attrib[
                                        attribute]

                # add the star name that the planet is in
                planet.nameStar = star.name
                planet.starObjectNamesToStar[star.name] = star
                planet.starObjectNamesToStar[''.join(
                    ch for ch in star.name if ch.isalnum()).lower()] = star

                starData = star.getData()
                # and others if there are any
                planet.otherNamesStar = star.otherNamesStar
                for starObject in star.otherNamesStar:
                    planet.starObjectNamesToStar[
                        starObject] = star
                    planet.starObjectNamesToStar[
                        ''.join(ch for ch in starObject if
                                ch.isalnum()).lower()] = star
                # add this planet to the list of planets in the star
                planets.append(planet)
                # and all planets list
                allPlanets.append(planet)
                # add the star reference in the planet
                planet.starObject = star

            # add the list of planets in the star to the star
            star.planetObjects = planets
            # add the name of the system that the star is in
            star.nameSystem = system.name
            star.systemObjectNamesToSystem[star.nameSystem] = system
            star.systemObjectNamesToSystem[
                ''.join(ch for ch in star.nameSystem if
                        ch.isalnum()).lower()] = system
            star.nameToPlanet = localPlanetsDict
            systemData = system.getData()
            # and others if there are any
            star.otherNamesSystem = system.otherNamesSystem
            for systemObject in system.otherNamesSystem:
                star.systemObjectNamesToSystem[
                    systemObject] = system
                star.systemObjectNamesToSystem[
                    ''.join(ch for ch in systemObject if
                            ch.isalnum()).lower()] = system
            # add the stars to the list of stars in the system
            stars.append(star)
            # and all stars list
            allStars.append(star)
            # add the system reference in the star
            star.systemObject = system
            # add the list of stars in the system to the system
            system.starObjects = stars
            system.nameToStar = localStarsDict
        # add the system to the list of all systems list
        allSystems.append(system)

    return (allSystems, allStars, allPlanets, allSystemsDict, allStarsDict,
            allPlanetsDict)
