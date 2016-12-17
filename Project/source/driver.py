#!/usr/bin/env python3.5

import getopt, sys, os

from driver_commands import *


def main():
    '''() -> NoneType
    Main driver method
    Accepts command line arguments
    Returns NoneType
    '''

    # flags which do not expect parameter (--help for example)
    # short opts are single characters, add onto shortOPT to include
    shortOPT = "huacel"
    # log opts are phrases, add onto longOPT to include
    longOPT = ["help", "update", "showall", "acceptall", "acceptall2",
               "denyall", "status", "postponeall", "clearblacklist",
               "stopautoupdate", "clearrepo", "fullreset"]

    # flags that do expect a parameter (--output file.txt for example)
    # similar to shortOPT
    shortARG = "sntdr"
    # similar to longOTP
    longARG = ["show", "accept", "accept2", "deny",
               "showrange", "postpone", "setautoupdate", "showlatest",
               "setrepo"]

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

    show_all_flag = False
    update_flag = False
    all_flag = False
    accept_all_flag = False
    accept_all2_flag = False
    accept_marker = None
    accept2_flag = False
    accept2_marker = None
    deny_all_flag = None
    postponeall_flag = None
    clearblacklist_flag = False
    stopautoupdate_flag = False
    setautoupdate_flag = False
    autoupdate_interval = None
    showlastest_flag = False
    showlastest_marker = None
    clearrepo_flag = False
    setrepo_flag = False
    repo_marker = None
    fullreset_flag = False

    # 0 for off, 1 for single select, 2 for range select
    show_flag = 0
    # 0 for off, 1 for single select, 2 for range select
    deny_flag = 0
    # 0 for off, 1 for single select, 2 for range select
    postpone_flag = 0
    # 0 for off, 1 for single select, 2 for range select
    accept_flag = 0
    # 0 for off, 1 for single select, 2 for range select
    accept2_flag = 0
    # list 1 element if single, 2 elements if range
    show_marker = None
    # list 1 element if single, 2 elements if range
    deny_marker = None
    # list 1 element if single, 2 elements if range
    postpone_marker = None

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


        # show
        elif o in ("-" + shortARG[0], "--" + longARG[0]):
            if ("-" in str(a)):
                show_flag = 2
                show_marker = str(a).split("-")
            else:
                show_flag = 1
                show_marker = [int(a)]


        # showall
        elif o in ("-" + shortOPT[2], "--" + longOPT[2]):
            show_all_flag = True

        # accept
        elif o in ("-" + shortARG[1], "--" + longARG[1]):
            if ("-" in str(a)):
                accept_flag = 2
                accept_marker = str(a).split("-")
            else:
                accept_flag = 1
                accept_marker = [int(a)]

        # accept2
        elif o in ("-" + shortARG[2], "--" + longARG[2]):
            if ("-" in str(a)):
                accept2_flag = 2
                accept2_marker = str(a).split("-")
            else:
                accept2_flag = 1
                accept2_marker = [int(a)]

        # acceptall
        elif o in ("-" + shortOPT[3], "--" + longOPT[3]):
            accept_all_flag = True

        # acceptall2
        elif o in ("-" + shortOPT[4], "--" + longOPT[4]):
            accept_all2_flag = True

        # deny
        elif o in ("-" + shortARG[3], "--" + longARG[3]):
            if ("-" in str(a)):
                # a range was specified
                deny_flag = 2
                deny_marker = str(a).split("-")
            else:
                # a single value was specified
                deny_flag = 1
                deny_marker = [int(a)]

        # denyall
        elif o in ("-" + shortOPT[5], "--" + longOPT[5]):
            deny_all_flag = True

        # status
        elif o in ("--" + longOPT[6]):
            status()

        # showrange
        elif o in ("-" + shortARG[4], "--" + longARG[4]):
            show_flag = True
            show_range_flag = True
            show_range_parameter = a

        # postpone
        elif o in ("--" + longARG[5]):
            if ("-" in str(a)):
                # a range was specified
                postpone_flag = 2
                postpone_marker = str(a).split("-")
            else:
                # a single value was specified
                postpone_flag = 1
                postpone_marker = [int(a)]

        # postponeall
        elif o in ("--" + longOPT[7]):
            postponeall_flag = True

        # clearblacklist
        elif o in ("--" + longOPT[8]):
            clearblacklist_flag = True

        # stopautoupdate
        elif o in ("--" + longOPT[9]):
            stopautoupdate_flag = True

        # setautoupdate
        elif o in ("--" + longARG[6]):
            setautoupdate_flag = True
            autoupdate_interval = int(a)

        # showlatest
        elif o in ("--" + longARG[7]):
            showlastest_flag = True
            showlastest_marker = int(a)

        # set repo
        elif o in ("--" + longARG[8]):
            setrepo_flag = True
            repo_marker = str(a)

        # clear repo
        elif o in ("--" + longOPT[10]):
            clearrepo_flag = True

        # fullreset
        elif o in ("--" + longOPT[11]):
            fullreset_flag = True

        else:
            usage()
            assert False, "unhandled option"

    # show all
    if (show_all_flag):
        show_all()

    # show
    if (show_flag == 2):
        try:
            startend = show_marker
            if startend[0].lower() == "s":
                start = "s"
            elif startend[0].lower() == "e":
                start = "e"
            else:
                start = int(startend[0])
            if startend[1].lower() == "e":
                end = "e"
            elif startend[1].lower() == "s":
                end = "s"
            else:
                end = int(startend[1])
            show_range(start, end)
        except:
            print("Invalid Range.")

    # show
    if (show_flag == 1):
        try:
            show_number(int(show_marker[0]))
        except ValueError:
            print("Invalid Parameter to shownumber.")

    # update
    if (update_flag):
        update()

    # accept
    if (accept_flag == 1):
        GIT.initGit()
        accept(accept_marker[0], 1)
        postpone_number(accept_marker[0])

    # accept range
    if (accept_flag == 2):
        GIT.initGit()
        try:
            if accept_marker[0].lower() == "s" or accept_marker[
                0].lower() == "e":
                start = accept_marker[0]
            else:
                start = int(accept_marker[0])
            if accept_marker[1].lower() == "s" or accept_marker[
                1].lower() == "e":
                end = accept_marker[1]
            else:
                end = int(accept_marker[1])
            accept_range(start, end, 1)
            postpone_range(start, end)
            print("Done.")
        except:
            print("Invalid Range")

    # accept all
    if (accept_all_flag):
        GIT.initGit()
        accept_all(1)
        postpone_all()
        print("Accepted all.")

    # accept2
    if (accept2_flag == 1):
        GIT.initGit2()
        accept(accept2_marker[0], 2)
        postpone_number((accept2_marker[0]))
        GIT.finalizeGit2()

    # accept2 range
    if (accept2_flag == 2):
        GIT.initGit2()
        try:
            if accept2_marker[0].lower() == "s" or accept2_marker[
                0].lower() == "e":
                start = accept2_marker[0]
            else:
                start = int(accept2_marker[0])
            if accept2_marker[1].lower() == "s" or accept2_marker[
                1].lower() == "e":
                end = accept2_marker[1]
            else:
                end = int(accept2_marker[1])
            accept_range(start, end, 2)
            postpone_range(start, end)
            print("Done.")
        except:
            print("Invalid Range")
        GIT.finalizeGit2()

    # accept all
    if (accept_all2_flag):
        GIT.initGit2()
        accept_all(2)
        GIT.finalizeGit2()
        postpone_all()
        print("Accepted all2")

    # deny
    if (deny_flag == 1):
        try:
            number = int(deny_marker[0])
            deny_number(number)
            print("Done.")
        except:
            print("Invalid Number")

    # deny range
    if (deny_flag == 2):
        try:
            if deny_marker[0].lower() == "s" or deny_marker[0].lower() == "e":
                start = deny_marker[0]
            else:
                start = int(deny_marker[0])
            if deny_marker[1].lower() == "s" or deny_marker[1].lower() == "e":
                end = deny_marker[1]
            else:
                end = int(deny_marker[1])
            deny_range(start, end)
            print("Done.")
        except:
            print("Invalid Range")

    # deny all
    if (deny_all_flag):
        deny_all()

    # postpone
    if (postpone_flag == 1):
        try:
            number = int(postpone_marker[0])
            postpone_number(number)
            print("Done.")
        except:
            print("Invalid Number")

    # postpone range
    if (postpone_flag == 2):
        try:
            if postpone_marker[0].lower() == "s" or postpone_marker[
                0].lower() == "e":
                start = postpone_marker[0]
            else:
                start = int(postpone_marker[0])
            if postpone_marker[1].lower() == "s" or postpone_marker[
                1].lower() == "e":
                end = postpone_marker[1]
            else:
                end = int(postpone_marker[1])
            postpone_range(start, end)
            print("Done.")
        except:
            print("Invalid Range")

    # postponeall
    if (postponeall_flag):
        postpone_all()

    # clearblacklist
    if (clearblacklist_flag):
        clearblacklist()

    # stopautoupdate
    if (stopautoupdate_flag):
        stopautoupdate()

    # setautoupdate
    if (setautoupdate_flag):
        setautoupdate(autoupdate_interval)

    # showlatest
    if (showlastest_flag):
        showlastest(showlastest_marker)

    # setrepo
    if (setrepo_flag):
        setrepo(repo_marker)

    # clearrepo
    if (clearrepo_flag):
        clearrepo()

    # fullreset
    if (fullreset_flag):
        fullreset()


if __name__ == "__main__":
    main()
