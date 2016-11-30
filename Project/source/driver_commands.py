#!/usr/bin/env python3.5

import getopt, sys, os
import data_retrieval.remoteGet as REM
import data_retrieval.apiGet as API
import data_parsing.XML_data_parser as XML
import data_parsing.CSV_data_parser as CSV
import data_comparison.Comparator as COMP
import data_comparison.proposed_change as PC
import github.gitClone as GIT
import storage_manager.storage_manager as STORAGE
import datetime
import subprocess
import urllib

# usage string
usage_str = "usage: driver --command [number | range]\n"

# link to NASA catalogue
NASA_link = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nsted\
API/nph-nstedAPI?table=exoplanets"

# link to exoplanet.eu catalogue
exoplanetEU_link = "http://exoplanet.eu/catalog/csv/"

# paths to NASA and EU csv files on local drive
nasa_file = "storage/nasa_csv"
EU_file = "storage/exoplanetEU_csv"

# path to XML .gz file
XML_path = "storage/OEC_XML.gz"

# list of all proposed changes (accumulated on update())
CHANGES = []

# the minimum autoupdate interval allowed (in hours)
MIN_AUTOU_INTERVAL = 1


def status():
    '''() -> NoneType
    Prints the current status of the updates, including the following
    relevant information: time of last update, current auto-update settings and
    the number of changes pending to be reviewed.
    '''

    unpack_changes()
    last_update = STORAGE.config_get("last_update")
    repo_url = STORAGE.config_get("repo_url")

    num_changes = len(CHANGES)
    if last_update == "Never":
        print("Last Update: Never" + "\n")
        print("Repo: " + repo_url)
    else:
        print("\nLast Update: " + str(last_update))
        print("Number of proposed changes stored : " + str(num_changes) + "\n")
        print("Repo: " + repo_url)


def usage():
    '''() -> NoneType
    Method for printing the usage string to the screen
    Returns NoneType
    '''

    print(usage_str)


def print_help():
    '''() -> NoneType
    Method for printing program manual to the screen
    '''

    print(STORAGE.manual())


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
    Method for showing all proposed changes
    '''

    unpack_changes()
    # sort the list of proposed changes    
    i = 1
    while i <= len(CHANGES):
        show_number(i)
        i += 1
    print("\nNumber of changes shown : " + str(len(CHANGES)))
    print("Last update : " + str(STORAGE.config_get("last_update")))
    # to reset last update time to default state ("Never"), and config file in
    # general : STORAGE.clean_config_file()
    print("End.\n")


def show_range(start, end):
    '''(int, int) -> NoneType
    or (str, str) -> NoneType, where str in [s,e]
    Method for showing a range of proposed changes between start and end
    Returns NoneType
    '''

    unpack_changes()
    # sort the list of proposed changes
    if isinstance(start, str) and start.lower() == "s":
        start = 1
    elif isinstance(start, str) and start.lower() == "e":
        start = len(CHANGES)
    if isinstance(end, str) and end.lower() == "e":
        end = len(CHANGES)
    elif isinstance(end, str) and end.lower() == "s":
        end = 1
    bothInts = isinstance(start, int) and isinstance(end, int)
    validRange = 1 <= start <= len(CHANGES) and 1 <= end <= len(CHANGES)
    if (bothInts and validRange):
        if start <= end:
            i = start
            while i <= end:
                show_number(i)
                i += 1
        else:  # start > end
            # reverse range
            i = start
            while i >= end:
                show_number(i)
                i -= 1
    else:
        print("Invalid range")


def show_number(n):
    '''(int) -> NoneType
    Method for showing the proposed change designated by 'n'
    '''

    if len(CHANGES) == 0:
        unpack_changes()
    if n <= len(CHANGES) and n > 0:
        print("\nShowing number : " + str(n) + "\n")
        print(str(CHANGES[n - 1]))
        print()
    else:
        print("Out of range.")


def accept(n, strategy):
    '''(int, int) -> NoneType
    Function for accepting a specific change/addition
    n argument is that change number to accept
    strategy argument accepts "1" or "2"
    Returns NoneType
    '''

    if len(CHANGES) == 0:
        unpack_changes()
    if n <= len(CHANGES) and n > 0:
        if (strategy == 1):
            GIT.modifyXML(CHANGES[n], n - 1)
        else:
            GIT.modifyXML(CHANGES[n], n - 1, mode=True)
    else:
        print("Out of range.")
    print("\nAccepted: \n" + str(n))


def accept_all(strategy):
    '''() -> NoneType
    Function for accepting all changes/additions
    strategy argument accepts "1" or "2"
    '''

    unpack_changes()
    i = 1
    while i <= len(CHANGES):
        accept(i, strategy)
        i += 1


def deny_number(n):
    '''(int) -> NoneType
    Method for declining a specific proposed changed, the one
    designated by 'n'
    Returns NoneType
    '''
    unpack_changes()
    if n > 0 and n <= len(CHANGES):
        # if given number is within the range, add the n-th change to black 
        # list and pop it from thelist of changes
        black_list = STORAGE.config_get("black_list")
        black_list.append(CHANGES.pop(n - 1))
        # update the blacklist
        STORAGE.config_set("black_list", black_list)
        # update the changes list in memory
        STORAGE.write_changes_to_memory(CHANGES)
        print("Done.")
    else:
        print("Out of range.")


def deny_range(start, end):
    '''(int, int) -> NoneType
    or (str, str) -> NoneType, where str in [s,e]
    Method for denying a range of proposed changes between start and end
    Returns NoneType
    '''
    global CHANGES
    unpack_changes()
    # sort the list of proposed changes
    if isinstance(start, str) and start.lower() == "s":
        start = 0
    elif isinstance(start, str) and start.lower() == "e":
        start = len(CHANGES)
    if isinstance(end, str) and end.lower() == "e":
        end = len(CHANGES)
    elif isinstance(end, str) and end.lower() == "s":
        end = 0
    bothInts = isinstance(start, int) and isinstance(end, int)
    validRange = 0 <= start <= len(CHANGES) and 0 <= end <= len(CHANGES)
    if (bothInts and validRange):
        black_list = STORAGE.config_get("black_list")
        for i in range(end, start - 1, -1):
            black_list.append(CHANGES.pop(i - 1))
            # update the blacklist
        STORAGE.config_set("black_list", black_list)
        # update the changes list in memory
        STORAGE.write_changes_to_memory(CHANGES)
    else:
        print("Invalid range")


def deny_all():
    '''() -> NoneType
    Method for declining all proposed changes.
    Returns NoneType
    '''
    unpack_changes()
    # add all currently pending changes to blacklist
    black_list = STORAGE.config_get("black_list")
    black_list.extend(CHANGES)
    # write black list to memory    
    STORAGE.config_set("black_list", black_list)
    # clear the list of currently pending changes
    STORAGE.write_changes_to_memory([])
    print("Done.")


def postpone_number(n):
    '''(int) -> NoneType
    Method for postponing a specific proposed changed, the one
    designated by 'n'
    Returns NoneType
    '''

    global CHANGES
    if len(CHANGES) == 0:
        unpack_changes()
    length = len(CHANGES)
    if n > 0 and n <= length:
        CHANGES.pop(n - 1)
        STORAGE.write_changes_to_memory(CHANGES)
    else:
        print("Out of range.")


def postpone_range(start, end):
    '''(int, int) -> NoneType
    or (str, str) -> NoneType, where str in [s,e]
    Method for postponing a range of proposed changes between start and end
    Returns NoneType
    '''
    global CHANGES
    unpack_changes()
    # sort the list of proposed changes
    if isinstance(start, str) and start.lower() == "s":
        start = 0
    elif isinstance(start, str) and start.lower() == "e":
        start = len(CHANGES)
    if isinstance(end, str) and end.lower() == "e":
        end = len(CHANGES)
    elif isinstance(end, str) and end.lower() == "s":
        end = 0
    bothInts = isinstance(start, int) and isinstance(end, int)
    validRange = 0 <= start <= len(CHANGES) and 0 <= end <= len(CHANGES)
    if (bothInts and validRange):
        indeces = set(range(start, end))
        CHANGES = [i for j, i in enumerate(CHANGES) if j not in indeces]
        STORAGE.write_changes_to_memory(CHANGES)

    else:
        print("Invalid range.")


def postpone_all():
    '''() -> NoneType
    Method for postponing all proposed changes.
    Returns NoneType
    '''
    STORAGE.write_changes_to_memory([])
    print("Done.")


def unpack_changes():
    '''
    () -> None
    
    Retrieves the list of ProposedChange objects from memory into global 
    variable "CHANGES".
    '''
    global CHANGES
    CHANGES = STORAGE.read_changes_from_memory()


def update():
    '''() -> NoneType
    Method for updating system from remote databases and generating
    proposed changes. Network connection required.
    Returns NoneType
    '''
    # postpone all currently pending changes
    STORAGE.write_changes_to_memory([])
    # open exoplanet catalogue
    global CHANGES
    CHANGES = []
    try:
        XML.downloadXML(XML_path)
    except urllib.error.URLError:
        print("No internet connection\n")
        return
    OEC_lists = XML.buildSystemFromXML(XML_path)
    OEC_systems = OEC_lists[0]
    OEC_stars = OEC_lists[1]
    OEC_planets = OEC_lists[2]

    # delete text files from previous update
    clean_files()

    # targets:
    # Saves nasa database into a text file named nasa_file
    NASA_getter = API.apiGet(NASA_link, nasa_file)
    try:
        NASA_getter.getFromAPI("&table=planets")
    # NASA_getter.getFromAPI("")
    except (TimeoutError, API.CannotRetrieveDataException) as e:
        print("NASA archive is unreacheable.\n")
    except (urllib.error.URLError):
        print("No internet connection.\n")

    # Saves exoplanetEU database into a text file named exo_file
    exoplanetEU_getter = API.apiGet(exoplanetEU_link, EU_file)
    try:
        exoplanetEU_getter.getFromAPI("")
    except (TimeoutError, API.CannotRetrieveDataException) as e:
        print("exoplanet.eu is unreacheable.\n")
    except (urllib.error.URLError):
        print("No internet connection.\n")

    # build the dict of stars from exoplanet.eu
    EU_stars = CSV.buildDictStarExistingField(EU_file, "eu")
    # build the dict of stars from NASA
    NASA_stars = CSV.buildDictStarExistingField(nasa_file, "nasa")
    # build the dictionary of stars from Open Exoplanet Catalogue
    OEC_stars = XML.buildSystemFromXML(XML_path)[4]

    # clean both dictionaries
    for d in [EU_stars, NASA_stars]:
        for key in d:
            if d.get(key).__class__.__name__ != "Star":
                d.pop(key)
    # retrieve the blacklist from memory
    black_list = STORAGE.config_get("black_list")
    # add chages from EU to the list (if they are not blacklisted by the user)
    for key in EU_stars.keys():
        if key in OEC_stars.keys():
            Comp_object = COMP.Comparator(EU_stars.get(key),
                                          OEC_stars.get(key), "eu")
            LIST = Comp_object.proposedChangeStarCompare()
            for C in LIST:
                if (not C in black_list) and (not C in CHANGES):
                    CHANGES.append(C)

    # add chages from NASA to the list
    for key in NASA_stars.keys():
        if key in OEC_stars.keys():
            Comp_object = COMP.Comparator(NASA_stars.get(key),
                                          OEC_stars.get(key), "nasa")
            LIST = Comp_object.proposedChangeStarCompare()
            for C in LIST:
                if (not C in black_list) and (not C in CHANGES):
                    CHANGES.append(C)

    # sort the list of proposed changes
    CHANGES = PC.merge_sort_changes(CHANGES)
    # write the list of proposed changes to memory using storage_manager
    STORAGE.write_changes_to_memory(CHANGES)
    # calculate current time
    curr_time = datetime.datetime.strftime(datetime.datetime.now(),
                                           '%Y-%m-%d %H:%M:%S')
    STORAGE.config_set("last_update", curr_time)
    print("\nNumber of differences discovered : " + str(len(CHANGES)))
    print("Current time : " + curr_time)
    print("Update complete.\n")


def clearblacklist():
    '''() -> NoneType
    
    Method for clearing declined blacklist of proposed changes
    '''
    STORAGE.config_set("black_list", [])
    print("Done.")


def showlastest(n):
    '''(int) -> NoneType
    Method for showest the lastest 'n' proposed changes
    "showlastest_marker" is passed in as int
    '''
    unpack_changes()

    if n >= 1 and n <= len(CHANGES):
        print("Showing the latest " + str(n) + " changes: ")
        newChanges = PC.sort_changes_lastupdate(CHANGES)
        i = 0
        while i < n:
            print("\nShowing number : " + str(newChanges[i]._index + 1) + "\n")
            print(str(newChanges[i]))
            print()
            i += 1
    else:
        print("Out of range.")
    pass


def setautoupdate(autoupdate_interval):
    '''(int) -> int
    Invokes the autoupdate_daemon to run in a seperate process
    autoupdate_daemon will continue to run after program exits
    Returns 0 if successful
    Returns 1 if invalid autoupdate interval
    '''

    if (autoupdate_interval >= MIN_AUTOU_INTERVAL):
        commandstr = "python3 autoupdate_daemon.py -i " + str(
            autoupdate_interval)
        subprocess.Popen(commandstr, shell=True)
        return 0
    else:
        print("Autoupdate interval too short!\n")
        return 1


def stopautoupdate():
    '''(int) -> NoneType
    Kills the autoupdate_daemon
    '''

    subprocess.call("pkill -f autoupdate_daemon.py", shell=True)


def setrepo(repo_name):
    '''(str) -> NoneType
    '''
    STORAGE.config_set("repo_url", repo_name)


def clearrepo():
    '''() -> NoneType
    '''
    STORAGE.config_set("repo_url", STORAGE.DEFAULT_REPO_URL)


def accept_range(start, end, strategy):
    '''(int, int, int) -> NoneType
    or (str, str, int) -> NoneType, where str in [s,e]
    Method for accepting a range of proposed changes between start and end
    where strategy designated the related strategy of accepting changes
    Returns NoneType
    '''
    unpack_changes()
    # sort the list of proposed changes
    if isinstance(start, str) and start.lower() == "s":
        start = 1
    elif isinstance(start, str) and start.lower() == "e":
        start = len(CHANGES)
    if isinstance(end, str) and end.lower() == "e":
        end = len(CHANGES)
    elif isinstance(end, str) and end.lower() == "s":
        end = 1
    bothInts = isinstance(start, int) and isinstance(end, int)
    validRange = 1 <= start <= len(CHANGES) and 1 <= end <= len(CHANGES)
    if (bothInts and validRange):
        if start <= end:
            i = start
            while i <= end:
                accept(i, strategy)
                i += 1
        else:  # start > end
            # reverse range
            i = start
            while i >= end:
                accept(i, strategy)
                i -= 1
    else:
        print("Invalid range")


def fullreset():
    '''
    () -> NoneType

    Clears all the settings set by the user; restores the program configuration
    to default state (Including list of stored proposed chages, autoupdate
    settings, target github repo url, etc.)
    '''
    stopautoupdate()
    STORAGE.reset_to_default()
