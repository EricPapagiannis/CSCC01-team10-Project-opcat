from subprocess import call
import xml.etree.ElementTree as ET
import data_comparison.proposed_change as PC
import os
import datetime
import storage_manager.storage_manager as STORAGE

# 'static' vars
files = []
direc = "github/open_exoplanet_catalogue"
link = STORAGE.config_get("repo_url")


def getLink():
    """ () -> str
    Return the link of the repository
    """
    return STORAGE.config_get("repo_url")


def getNextBranchNumber():
    """ () -> int
    Return the next valid branch number, and increment the next branch so it is
    valid still
    """
    branch_number = STORAGE.config_get("branch_number")
    STORAGE.config_set("branch_number", branch_number + 1)
    return branch_number


def getCurrentBranchNumber():
    """ () -> int
    Return the current branch number, without incrementing it
    """
    return STORAGE.config_get("branch_number") - 1


def initGit():
    ''' () -> None
    Does any initialization to use github with strategy 1
    '''
    # change to actual repository later
    global link
    call(["git", "--bare", "clone", getLink()], cwd="github")
    link = getLink().split('/')[-1][0:-4]
    call(["git", "remote", "add", "upstream",
          getLink()],
         cwd=direc)
    call(["git", "push", "--set-upstream", "origin", "master"], cwd=direc)
    call(["git", "checkout", "master"], cwd=direc)
    return link


def initGit2():
    ''' () -> None
    Does any initialization to use github with strategy 1
    '''
    global link
    branch = "OPCAT" + str(getNextBranchNumber())
    call(["git", "--bare", "clone", getLink()], cwd="github")
    link = getLink().split('/')[-1][0:-4]
    call(["git", "remote", "add", "upstream",
          getLink()],
         cwd=direc)
    call(["git", "push", "--set-upstream", "origin", "master"], cwd=direc)
    call(["git", "checkout", "master"], cwd=direc)
    call(["git", "checkout", "-b", branch], cwd=direc)
    call(["git", "push", "upstream", branch], cwd=direc)
    return link


def finalizeGit2():
    """ () -> None
    Does any final commands to use github with strategy 2
    """
    branch = "OPCAT" + str(getCurrentBranchNumber())
    print("Performing cleanup...")
    call(["python3", "cleanup.py"], cwd="github")
    call(["git", "add", "systems"], cwd=direc)
    call(["git", "commit", "-m", "Cleanup"], cwd=direc)
    print("...Cleanup complete")

    call(["git", "push", "upstream", branch], cwd=direc)

    # pull-request
    call(["hub", "pull-request", "-f", "-h", branch, "-m",
          "Compiled modifications"], cwd=direc)


def saveDirName(direc):
    """ (str) -> None
    Save the directory name for the repo
    """
    file = open('dirname', 'w')
    file.write(direc)
    file.close()


def getDirName():
    """ () -> None
        Get the directory name for the repo
    """
    try:
        file = open('dirname', 'r')
        return file.read()
    except IOError:
        return None


def UpdateRepo():
    """ () -> None
    Update the the local github repo to latest
    """
    # check for local github repo
    direc = getDirName()
    if (direc == None):
        direc = initGit()
        saveDirName(direc)

    # updating github repo
    call(["git", "fetch"], cwd=direc)
    call(["git", "pull"], cwd=direc)
    # commit process
    # require login info first
    # call(["git", "add", "."] + files, cwd=direc)
    # call(["git", "commit", "-m", "automated commit"], cwd=direc)
    # call(["git", "push"], cwd=direc)


def modifyXML(proposedChange, n, mode=False):
    """ (ProposedChange, int, bool) -> None
    Given a proposed change, and the a number n referring to what proposed
    change it is, apply the github pull request strategy depending on mode.
    mode = False represents strategy 1: 1 branch per modification and 1 pull
        request per branch
    mode = True represents strategy 2: 1 branch witl all modifications, and 1
        pull request
    """
    # case if proposed change is modification
    if isinstance(proposedChange, PC.Modification):
        path = "github/open_exoplanet_catalogue/systems/" + \
               proposedChange.getSystemName() + ".xml"
        path2 = "systems/" + proposedChange.getSystemName() + ".xml"
        oec = ET.parse(path)
        # apply strategy 2
        if mode:
            branch = "opcat" + str(getCurrentBranchNumber())
            # if the proposed change is a star, modify the star fields
            if proposedChange.getOECType() == "Star":
                # modify
                modifyStar(oec, proposedChange)
                # commit
            # if the proposed change is a planet, modify the planet fields
            elif proposedChange.getOECType() == "Planet":
                # modify
                modifyPlanet(oec, proposedChange)
                # commit
            call(["git", "add", path2], cwd=direc)
            commitMessage = str(proposedChange)
            call(["git", "commit", "-m", commitMessage], cwd=direc)
        # apply strategy 1
        else:
            branch = "opcat" + str(getNextBranchNumber())
            # if the proposed change is a star, modify the star fields
            call(["git", "checkout", "master"], cwd=direc)
            call(["git", "checkout", "-b", branch], cwd=direc)
            call(["git", "push", "upstream", branch], cwd=direc)
            # modify
            if proposedChange.getOECType() == "Star":
                modifyStar(oec, proposedChange)
                # commit
            # if the proposed change is a planet, modify the planet fields
            elif proposedChange.getOECType() == "Planet":
                # modify
                modifyPlanet(oec, proposedChange)
            # commit
            path2 = "systems/" + proposedChange.getSystemName() + ".xml"
            call(["git", "add", path2], cwd=direc)
            commitMessage = str(proposedChange)

            call(["git", "commit", "-m", commitMessage, path2], cwd=direc)
            print("Performing cleanup...")
            call(["python3", "cleanup.py"], cwd="github")
            call(["git", "commit", "-m", "Cleanup", path2], cwd=direc)
            print("...Cleanup complete")
            call(["git", "push", "upstream", branch], cwd=direc)
            # pull-request
            call(["hub", "pull-request", "-f", "-h", branch, "-m",
                  commitMessage], cwd=direc)


def modifyStar(oec, proposedChange):
    """ (ElementTree, ProposedChange) -> None
    Given the XML for the related proposed change, and a ProposedChange for a
    star, apply the modifications of the proposed change into the XML
    """
    specificStarXML = None
    path = "github/open_exoplanet_catalogue/systems/" + \
           proposedChange.getSystemName() + ".xml"
    # find the star we want
    for starXML in oec.findall(".//star"):
        for child in starXML.findall(".//name"):
            if child.text == proposedChange.get_object_name():
                specificStarXML = starXML

    # now modify our data field we want
    child = specificStarXML.find(".//" + str(proposedChange.field_modified))
    child.text = str(proposedChange.value_in_origin_catalogue)
    oec.write(path)
    modifyDateToCurrent(oec, proposedChange)


def modifyDateToCurrent(oec, proposedChange):
    """(ElementTree) -> None
    Given the XML for the related proposed change, modify the date to be the
    current date
    """
    path = "github/open_exoplanet_catalogue/systems/" + \
           proposedChange.getSystemName() + ".xml"
    child = oec.find(".//lastupdate")
    child.text = datetime.datetime.strftime(datetime.datetime.now(),
                                            '%Y/%m/%d')[2:]
    oec.write(path)


def modifyPlanet(oec, proposedChange):
    """ (ElementTree, ProposedChange) -> None
    Given the XML for the related proposed, and a ProposedChange for a star,
    apply the modifications of the proposed change into the XML
    """
    specificPlanetXML = None
    path = "github/open_exoplanet_catalogue/systems/" + \
           proposedChange.getSystemName() + ".xml"
    # find the planet we want
    for planetXML in oec.findall(".//planet"):
        for child in planetXML.findall(".//name"):
            if child.text == proposedChange.get_object_name():
                specificPlanetXML = planetXML

    # now modify our data field we want
    child = specificPlanetXML.find(".//" + str(proposedChange.field_modified))
    child.text = str(proposedChange.value_in_origin_catalogue)
    # modify the related error bounds if they exist
    if proposedChange.origin_upper != "N/A" and proposedChange.upper_attrib_name != "N/A":
        if proposedChange.OEC_upper != "N/A" and float(
                proposedChange.OEC_upper) != float(proposedChange.origin_upper):
            child.attrib[
                proposedChange.upper_attrib_name] = proposedChange.origin_upper
        elif proposedChange.OEC_upper == "N/A":
            child.attrib[
                proposedChange.upper_attrib_name] = proposedChange.origin_upper
    if proposedChange.origin_lower != "N/A" and proposedChange.lower_attrib_name != "N/A":
        if proposedChange.OEC_lower != "N/A" and float(
                proposedChange.OEC_lower) != float(proposedChange.origin_lower):
            child.attrib[
                proposedChange.lower_attrib_name] = proposedChange.origin_lower
        elif proposedChange.OEC_lower == "N/A":
            child.attrib[
                proposedChange.lower_attrib_name] = proposedChange.origin_lower
    oec.write(path)
    # update the date to the current
    modifyDateToCurrent(oec, proposedChange)
