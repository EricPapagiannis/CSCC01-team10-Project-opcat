#!/usr/bin/env python3.5

import getopt, sys, os
import data_retrieval.remoteGet as REM
import data_retrieval.apiGet as API
import data_parsing.XML_data_parser as XML
import data_parsing.CSV_data_parser as CSV

help_string = "Opcat version 0.1\nBasic operation:\n$ driver --update   \
Retrieves data from target catalogues (NASA, openexoplanet.eu) as a list of \
starsystems. Retrieves data from the github database of Open Exoplanet \
catalogue as a separate list of star systems. Compares the two lists, \
building a list of proposed changes. (Not implemented yet) After update \
is complete the user can view proposed changes. (Not implemented yet)\n\n"


NASA_link = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nsted\
API/nph-nstedAPI?table=exoplanets"

exoplanetEU_link = "http://exoplanet.eu/catalog/csv/"

nasa_file = "nasa_csv"
EU_file = "exoplanetEU_csv"

all_tags = ["mass", "radius", "period", "semimajoraxis", "discoveryyear", \
            "lastupdate", "discoverymethod", "eccentricity"]

def usage():
    '''() -> NoneType
    Example called method
    Returns NoneType
    '''
    print("usage: driver [--help] [--update] [--output string] " +
    "[--planet string] [--showall | --shownumber int]\n")


def print_help():
    '''() -> NoneType
    '''
    print(help_string)


def clean_files():
    '''() -> NoneType
    Removes text files from previous update.
    Returns None
    '''
    for name in [nasa_file, EU_file]:
        try:
            os.remove(name)
        except:
            pass
	

def show_all():
    '''() -> NoneType
    Skeleton function
    '''
    print("showed all")


def show_number(show_parameter):
    '''() -> NoneType
    Skeleton function
    '''
    print(show_parameter + " showed")


def update():
    '''() -> NoneType
    Example called method
    Returns NoneType
    '''
    # open exoplanet catalogue
    OEC_lists = XML.buildSystemFromXML()
    OEC_systems = OEC_lists[0]
    OEC_stars = OEC_lists[1]
    OEC_planets = OEC_lists[2]
    # delete text files from previous update
    #clean_files()
    
    
    '''
    # targets:
    # Saves nasa database into a text file named nasa_file
    NASA_getter = API.apiGet(NASA_link, nasa_file)
    try:
        NASA_getter.getFromAPI("&table=planets")
    except (TimeoutError, API.CannotRetrieveDataException) as e:
        print("NASA archive is unreacheable.\n")
    # Saves exoplanetEU database into a text file named exo_file
    exoplanetEU_getter = API.apiGet(exoplanetEU_link, EU_file)
    try:
        exoplanetEU_getter.getFromAPI("")
    except (TimeoutError, API.CannotRetrieveDataException) as e:
        print("exoplanet.eu is unreacheable.\n")
    '''
    
    
    # build the dict of stars from exoplanet.eu
    EU_stars = CSV.buildDictStarExistingField(EU_file, "eu")
    # build the dict of stars from NASA
    NASA_stars = CSV.buildDictStarExistingField(nasa_file, "nasa")
    # build the dictionary of stars from Open Exoplanet Catalogue
    OEC_stars = {}
    
    
    for curr in [EU_stars, NASA_stars] :
        print(curr.keys())
        print()
    
    
    
    
    
    '''
    EU_stars = CSV.buildListPlanets(exo_file, all_tags, "eu")


    q = CSV.buildListPlanetsAllField(EU_file, "eu")
    qq = CSV.buildListPlanetsAllField(nasa_file, "nasa")
    
    for l in [q, qq] :
        for planet in q :
            print(planet)



    i = 0
    while i < 10 :
        try:
            print(EXO_planets[i])
            print()
        except:
            pass
        i += 1
    
    i = 0
    while i < 10 :
        try:
            print(OEC_planets[i])            
            print()
        except:
            pass
        i += 1
    
    
    # print all)
    for planet in OEC_planets :
        try:
            print(planet)
            print()
        except:
            pass
    print("\n\n\n")
    print("First 100 Planet objects from Open Exoplanet Catalogue and from"+\
          " exoplanet.eu are displayed.")
    print("Number of planet objects retrieved: " + str(len(OEC_planets)) +\
          " From Open Exoplanet Catalogue; " + str(len(EXO_planets)) +\
          " from exoplanet.eu")
    '''
    
    
    
    
    print("Update complete.\n")


def main():
    '''() -> NoneType
    Main driver method
    Accepts command line arguments
    Returns NoneType
    '''
    # flags which do not expect parameter (--help for example)
    # short opts are single characters, add onto shortOPT to include
    shortOPT = "hua"
    # log opts are phrases, add onto longOPT to include
    longOPT = ["help", "update", "showall"]

    # flags that do expect a parameter (--output file.txt for example)
    # similar to shortOPT
    shortARG = "ops"
    # similar to longOTP
    longARG = ["output", "planet", "shownumber"]

    # arg, opt pre-processor, do not edit
    short = ':'.join([shortARG[i:i + 1] for i in range(0, len(shortARG), 1)]) \
            + ":" + shortOPT
    long = [arg + "=" for arg in longARG] + longOPT

    try:
        opts, args = getopt.getopt(sys.argv[1:], short, long)
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    output = None
    planet = None
    show_parameter = None
    update_flag = False
    show_flag = False
    all_flag = False

    for o, a in opts:

        # handles args and opts
        # a contains parameter for ARGs, not OPTs

	# help
        if o in ("-" + shortOPT[0], "--" + longOPT[0]):
            print_help()
            sys.exit()

	# update
        elif o in ("-" + shortOPT[1], "--" + longOPT[1]):
            update_flag = True

	# output
        elif o in ("-" + shortARG[0], "--" + longARG[0]):
            output = a

	# planet
        elif o in ("-" + shortARG[1], "--" + longARG[1]):
            planet = a

        # shownumer
        elif o in ("-" + shortARG[2], "--" + longARG[2]):
            show_flag = True
            show_parameter = a

        # showall
        elif o in ("-" + shortOPT[2], "--" + longOPT[2]):
            show_flag = True
            all_flag = True

        else:
            usage()
            assert False, "unhandled option"
	
    if (show_flag):
        if ((all_flag) and (show_parameter)):
            print_help()
            return 1
        elif (all_flag):
            show_all()
        else:
            show_number(show_parameter)

    # update
    if (update_flag):
        update()
	
    '''
    if (output):
        print("output: " + output)
    if (planet):
        print("planet specified: " + planet)
    '''


if __name__ == "__main__":
    main()
