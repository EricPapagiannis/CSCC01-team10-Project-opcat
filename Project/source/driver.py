#!/usr/bin/env python3.5

import getopt, sys
import data_retrieval.apiGet as API
import data_parsing.XML_data_parser as XML


help_string = "Opcat version 0.1\nBasic operation:\n$ driver --update   \
Retrieves data from target catalogues (NASA, openexoplanet.eu) as a list of \
starsystems. Retrieves data from the github database of Open Exoplanet \
catalogue as a separate list of star systems. Compares the two lists, \
building a list of proposed changes. (Not implemented yet) After update \
is complete the user can view proposed changes. (Not implemented yet)\n\n"


def usage():
    '''() -> NoneType
    Example called method
    Returns NoneType
    '''
    print("usage: driver --help | --update \n")
    #print("usage: driver -h | -u | -o string | -p string\n")

def help():
    print(help_string)

def update():
    '''() -> NoneType
    Example called method
    Returns NoneType
    '''
    
    # open exoplanet cat
    OEC_lists = XML.buildSystemFromXML()
    
    OEC_systems = OEC_lists[0]
    OEC_stars = OEC_lists[1]
    OEC_planets = OEC_lists[2]
    
    # targets:
    #API_getter = API.apiGet("", "TEMP")
    

    print("Update complete.\n")


def main():
    '''() -> NoneType
    Main driver method
    Accepts command line arguments
    Returns NoneType
    '''
    # flags which do not expect parameter (--help for example)
    # short opts are single characters, add onto shortOPT to include
    shortOPT = "hu"
    # log opts are phrases, add onto longOPT to include
    longOPT = ["help", "update"]

    # flags that do expect a parameter (--output file.txt for example)
    # similar to shortOPT
    shortARG = "op"
    # similar to longOTP
    longARG = ["output", "planet"]

    # arg, opt pre-processor, do not edit
    short = ':'.join([shortARG[i:i + 1] for i in range(0, len(shortARG), 1)])\
        + ":" + shortOPT
    long = ["=" + arg for arg in longARG] + longOPT

    try:
        opts, args = getopt.getopt(sys.argv[1:], short, long)
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    output = None
    planet = None
    update_flag = False

    for o, a in opts:

        # handles args and opts
        # a contains parameter for ARGs, not OPTs
        if o in ("-" + shortOPT[0], "--" + longOPT[0]):
            help()
            sys.exit()

        elif o in ("-" + shortOPT[1], "--" + longOPT[1]):
            update_flag = True

        elif o in ("-" + shortARG[0], "--" + longARG[0]):
            output = a

        elif o in ("-" + shortARG[1], "--" + longARG[1]):
            planet = a

        else:
            usage()
            assert False, "unhandled option"

    # processing example
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
