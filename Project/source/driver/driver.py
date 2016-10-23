import getopt
import sys


def usage():
    '''() -> NoneType
    Example called method
    Returns NoneType
    '''

    print("usage: driver -h | -v | -o string | -p string\n")


def update():
    '''() -> NoneType
    Example called method
    Returns NoneType
    '''

    print("updating...\n")


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
    short = ':'.join([shortARG[i:i + 1] for i in range(0, len(shortARG), 1)]) + ":" + shortOPT
    long = ["=" + arg for arg in longARG] + longOPT

    try:
        opts, args = getopt.getopt(sys.argv[1:], short, long)
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    output = None
    planet = None
    update = False

    for o, a in opts:

        # handles args and opts
        # a contains parameter for ARGs, not OPTs
        if o in ("-" + shortOPT[0], "--" + longOPT[0]):
            usage()
            sys.exit()

        elif o in ("-" + shortOPT[1], "--" + longOPT[1]):
            update = True

        elif o in ("-" + shortARG[0], "--" + longARG[0]):
            output = a

        elif o in ("-" + shortARG[1], "--" + longARG[1]):
            planet = a

        else:
            assert False, "unhandled option"

    # processing example
    if (update):
        update()
    if (output):
        print("output: " + output)
    if (planet):
        print("planet specified: " + planet)


if __name__ == "__main__":
    main()
