import gzip
import io
import urllib.request
import xml.etree.ElementTree as ET

from Planet import *
from PlanetaryObject import *
from System import *

from data_parsing.Star import *

url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))


# returns a tuple of a (list of all system objects, list of star objects, list of all planet objects)
# system has reference to its stars
# stars has reference to its planets

# planets have reference to the star and system it is in
# stars have reference to the system it is in
def buildSystemFromXML():
    allSystems = []
    allStars = []
    allPlanets = []
    for systemXML in oec.findall(".//system"):
        i = 0
        for child in systemXML.findall(".//name"):
            if child.tag == "name":
                if i == 0:
                    systemName = child.text
                    system = System(systemName)
                elif i == 1:
                    system.addValList("otherNamesSystem", child.text)
                else:
                    system.addToValList("otherNamesSystem", child.text)
                i += 1
            else:
                system.addToValList("otherNamesSystem", child.text)

        for child in systemXML:
            if (child.tag.lower() != "star") and (child.tag.lower() != "name"):
                system.addVal(child.tag, child.text)

        stars = []
        for starXML in systemXML.findall(".//star"):
            ii = 0
            for child in starXML.findall(".//name"):
                if child.tag == "name":
                    if ii == 0:
                        star = Star(child.text)
                        system.addValList("stars", child.text)
                    elif ii == 1:
                        star.addValList("otherNamesStar", child.text)
                    else:
                        star.addToValList("otherNamesStar", child.text)
                    ii += 1
                else:
                    star.addToValList("otherNamesStar", child.text)

            for child in starXML:
                if (child.tag.lower() != "planet") and (child.tag.lower() != "name"):
                    star.addVal(child.tag, child.text)

            planets = []
            for planetXML in starXML.findall(".//planet"):
                iii = 0
                for child in planetXML.findall(".//name"):
                    if child.tag == "name":
                        if iii == 0:
                            planet = Planet(child.text)
                            star.addValList("planets", child.text)
                        elif iii == 1:
                            planet.addValList("otherNamesPlanet", child.text)
                        else:
                            planet.addToValList("otherNamesPlanet", child.text)
                        iii += 1
                    else:
                        planet.addToValList("otherNamesPlanet", child.text)

                for child in planetXML:
                    if (child.tag.lower() != "name"):
                        planet.addVal(child.tag, child.text)

                planet.addVal("nameSystem", system.getVal("nameSystem"))
                systemData = system.getData()
                if "otherNamesSystem" in systemData:
                    planet.addValList("otherNamesSystem", systemData["otherNamesSystem"])

                planet.addVal("nameStar", star.getVal("nameStar"))
                starData = star.getData()

                if "otherNamesStar" in starData:
                    planet.addValList("otherNamesStar", starData["otherNamesStar"])
                planets.append(planet)
                allPlanets.append(planet)
                planet.addVal("starObject", star)
                planet.addVal("systemObject", system)
                star.addValList("planetObjects", planets)
                print("PLANET: ", planet)

            star.addVal("nameSystem", system.getVal("nameSystem"))
            star.addValList("otherNamesSystem", system.getVal("otherNamesSystem"))
            stars.append(star)
            allStars.append(star)
            star.addVal("systemObject", system)
            system.addValList("starObjects", stars)
            print("STAR: ", star)

        allSystems.append(system)
        print("SYSTEM: ", system)
        print('\n\n')

    return (allSystems, allStars, allPlanets)


buildSystemFromXML()
