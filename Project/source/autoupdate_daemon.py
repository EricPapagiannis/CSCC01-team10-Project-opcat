import time
import sys
import getopt
import subprocess

# This is the autoupdater daemon
# Do not use directly


# Verbose mode
# By default, daemon does not output to stdout
VERBOSE = True


class InvalidIntervalException(Exception):
    pass


def main():
    sleeptime = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:")
    except getopt.GetoptError:
        print(sys.argv)
        print("autoupdate_daemon.py -i hours")
        sys.exit(2)
    for opt, arg, in opts:
        if opt == "-i":
            sleeptime = int(arg)

    if (sleeptime > 0):
        # convert hours to seconds
        sleeptime_hours = sleeptime * 3600
    else:
        raise InvalidIntervalException("Interval must be 1 hour or greater")

    # command to call driver.py's update method
    commandstr = "python3 driver.py --update"

    while (1):
        # daemon continues to run until it is killed by driver
        if (VERBOSE):
            print("Updating...")
        subprocess.Popen(commandstr, shell=True)
        time.sleep(sleeptime_hours)


if __name__ == "__main__":
    main()
