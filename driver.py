import getopt, sys

def usage():
    print("usage: app @TODO");

def main():

    # flags which do not expect parameter (--help for example)
    shortOPT = "hv"
    longOPT = ["help", "verbose"]
    
    # flags that do expect a parameter (--output file.txt for example)
    shortARG = "op"
    longARG = ["output", "planet"]
    
    # arg, opt pre-processor, do not edit
    short = ':'.join([shortARG[i:i+1] for i in range(0, len(shortARG), 1)]) + \
    ":" + shortOPT
    long = ["=" + arg for arg in longARG] + longOPT

    try:
        opts, args = getopt.getopt(sys.argv[1:], short, long)
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    output = None
    planet = None
    verbose = False
    for o, a in opts:

        # handles args and opts
        if o in ("-" + shortOPT[0], "--" + longOPT[0]):
            usage()
            sys.exit()
        elif o in ("-" + shortOPT[1], "--" + longOPT[1]):
            verbose = True
        elif o in ("-" + shortARG[0], "--" + longARG[0]):
            output = a
        elif o in ("-" + shortARG[1], "--" + longARG[1]):
            planet = a
        else:
            assert False, "unhandled option"

    # additional processing
    if (verbose):
        print ("verbose mode")
    if (output):
        print ("output: " + output)
    if (planet):
        print ("planet: " + planet)

if __name__ == "__main__":
    main()