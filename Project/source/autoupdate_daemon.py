import time
import sys
import getopt

# This is the autoupdater daemon
# Do not use directly

def main():
    
    sleeptime = 0
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:")
    except getopt.GetoptError:
        print(sys.argv)
        print ("autoupdate_daemon.py -i hours")
        sys.exit(2)
    for opt, arg, in opts:
        if opt == "-i":
            sleeptime = int(arg)

    time.sleep(sleeptime)
    f = open("placeholder.txt","w")
    f.write("placeholder")
    f.close()

if __name__ == "__main__":
    main()
