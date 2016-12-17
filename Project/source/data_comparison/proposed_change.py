from datetime import datetime as dt


class ProposedChange:
    '''
    Abstract class. Not used directly. Parent Class of Addition and 
    Modicfication
    
    origin must be one of {"NASA archive", "exoplanet.eu"}
    '''

    def __init__(self, origin):
        self.origin = origin


class Addition(ProposedChange):
    '''
    object_ptr is the pointer to PlanetaryObject instance to be added.
    '''

    def __init__(self, origin, object_ptr):
        self.object_ptr = object_ptr
        self.lastupdate = object_ptr.lastupdate
        ProposedChange.__init__(self, origin)

    def __str__(self):
        s = "Proposed addition:\n\n"
        s += "Name of object added : "
        s += self.object_ptr.name
        s += "\nOrigin : "
        s += str(self.origin)
        s += "\n"
        s += "Type of object: "
        s += self.object_ptr.__class__.__name__
        s += "\n"
        s += "Last modified by "
        s += str(self.origin)
        s += " on: "
        s += self.lastupdate
        s += "\n"
        s += "Stats:\n"
        s += str(self.object_ptr)
        s += "\n"
        return s

    def fancyStr(self):
        return str(self)

    def __eq__(self, other):
        return (
            (type(other) is type(self)) and (self.origin == other.origin) and (
                self.object_ptr.name == other.object_ptr.name) and (
                self.object_ptr.data == other.object_ptr.data))

    def __ne__(self, other):
        return not (self == other)

    def get_object_name(self):
        '''
        () -> str
        
        Returns the name of the PlanetaryObject to which this instance of 
        proposed addition is referring.
        '''
        if self.object_ptr is not None:
            return self.object_ptr.name
        else:
            return ""


class Modification(ProposedChange):
    '''
    target_system_ptr is the pointer to PlanetaryObject instance originating 
    from one of target catalogues (NASA, exoplanet.eu). OEC_system_ptr is the 
    pointer to planetary object originating from Open Exoplanet Catalogue.
    
    target_system_ptr and OEC_system_ptr must be of the same subclass; ex: both
    Star objects or both Planet objects
    
    field_modified is the name of the field modified.
    value_in_origin_catalogue / value_in_OEC - may or may not be of type str
    '''

    def __init__(self, origin, OEC_object, origin_object,
                 field_modified, value_in_origin_catalogue, value_in_OEC):
        self.OEC_object = OEC_object
        self.origin_object = origin_object
        self.lastupdate = origin_object.lastupdate
        self.field_modified = field_modified
        self.value_in_origin_catalogue = value_in_origin_catalogue
        self.value_in_OEC = value_in_OEC

        limits = self.getUpperLowerAttribs()
        self.OEC_upper = limits[0]
        self.OEC_lower = limits[1]
        self.origin_upper = limits[2]
        self.origin_lower = limits[3]
        self.upper_attrib_name = limits[4]
        self.lower_attrib_name = limits[5]
        self._index = None
        ProposedChange.__init__(self, origin)

    def __eq__(self, other):
        """ (ProposedChange) -> bool
        Return a comparison between the self proposed change and the other
        proposed change
        """
        return (
            (type(other) is type(self)) and (self.origin == other.origin) and (
                self.OEC_object.name == other.OEC_object.name) and (
                str(self.OEC_object.__class__.__name__) == str(
                    other.OEC_object.__class__.__name__)) and (
                self.getSystemName() == other.getSystemName()) and (
                self.field_modified == other.field_modified) and (
                self.lastupdate == other.lastupdate) and (
                self.value_in_OEC == other.value_in_OEC) and (
                self.value_in_origin_catalogue == other.value_in_origin_catalogue) and (
                self.OEC_upper == other.OEC_upper) and (
                self.OEC_lower == other.OEC_lower) and (
                self.origin_upper == other.origin_upper) and (
                self.origin_lower == other.origin_lower) and (
                self.upper_attrib_name == other.upper_attrib_name) and (
                self.lower_attrib_name == other.lower_attrib_name))

    def __ne__(self, other):
        return not (self == other)

    def getUpperLowerAttribs(self):
        """() -> (str, str, str,  str, str)
        Return the upper and lower limit attributes of the numeric field
        Returned as (OEC_upper, OEC_lower, origin_upper, origin_lower, fieldName)
        """
        upperAttribs = ["errorplus", "upperlimit"]
        lowerAttribs = ["errorminus", "lowerlimit"]
        OEC_upper = 'N/A'
        OEC_lower = 'N/A'
        origin_upper = 'N/A'
        origin_lower = 'N/A'
        upperAttribName = "N/A"
        lowerAttribName = "N/A"
        for field in self.OEC_object.errors:
            if self.field_modified in field and self.field_modified != field:
                if field[len(self.field_modified):] in upperAttribs:
                    upperAttribName = field[len(self.field_modified):]
                    OEC_upper = self.OEC_object.errors[field]
                if field[len(self.field_modified):] in lowerAttribs:
                    lowerAttribName = field[len(self.field_modified):]
                    OEC_lower = self.OEC_object.errors[field]

        for field in self.origin_object.errors:
            if self.field_modified in field and self.field_modified != field:
                if field[len(self.field_modified):] in upperAttribs:
                    upperAttribName = field[len(self.field_modified):]
                    origin_upper = self.origin_object.errors[field]
                if field[len(self.field_modified):] in lowerAttribs:
                    lowerAttribName = field[len(self.field_modified):]
                    origin_lower = self.origin_object.errors[field]
        if OEC_upper == "":
            OEC_upper = "N/A"
        if OEC_lower == "":
            OEC_lower = "N/A"
        if origin_upper == "":
            origin_upper = "N/A"
        if origin_lower == "":
            origin_lower = "N/A"
        if upperAttribName == "":
            upperAttribName = "N/A"
        if lowerAttribName == "":
            lowerAttribName = "N/A"
        return (
            OEC_upper, OEC_lower, origin_upper, origin_lower, upperAttribName,
            lowerAttribName)

    def __str__(self):
        s = "Proposed modification:\n\n"
        s += "Name of object modified: "
        s += self.OEC_object.name
        s += "\nOrigin : "
        s += str(self.origin)
        s += "\n"
        s += "Type of object modified: "
        s += str(self.OEC_object.__class__.__name__)
        s += "\n"
        if self.OEC_object.__class__.__name__ != "System":
            s += "Part of System: "
            if self.OEC_object.__class__.__name__ == "Star":
                s += self.OEC_object.nameSystem
            elif self.OEC_object.__class__.__name__ == "Planet":
                s += self.OEC_object.starObject.nameSystem
            s += "\n"
        s += "Field modified: "
        s += str(self.field_modified)
        s += "\n"
        s += "Last modified by "
        s += str(self.origin)
        s += " on: "
        s += self.lastupdate
        s += "\n"
        s += "Value according to "
        s += str(self.origin)
        s += ": "
        s += str(self.value_in_origin_catalogue)
        s += "\n"
        s += "Value according to Open Exoplanet Catalogue: "
        s += str(self.value_in_OEC)
        s += "\n"
        s += "OEC Upper Limit: "
        s += str(self.OEC_upper)
        s += "\n"
        s += "OEC Lower Limit: "
        s += str(self.OEC_lower)
        s += "\n"
        s += "Origin Upper Limit: "
        s += str(self.origin_upper)
        s += "\n"
        s += "Origin Lower Limit: "
        s += str(self.origin_lower)
        s += "\n"
        return s

    def fancyStr(self):
        """ () -> str
        Return a fancier, coloured version of __str__()
        """
        s = "Proposed modification:\n\n"
        s += "Name of object modified: "
        s += self.OEC_object.name
        s += "\nOrigin : "
        s += str(self.origin)
        s += "\n"
        s += "Type of object modified: "
        s += str(self.OEC_object.__class__.__name__)
        s += "\n"
        if self.OEC_object.__class__.__name__ != "System":
            s += "Part of System: "
            if self.OEC_object.__class__.__name__ == "Star":
                s += self.OEC_object.nameSystem
            elif self.OEC_object.__class__.__name__ == "Planet":
                s += self.OEC_object.starObject.nameSystem
            s += "\n"
        s += "Field modified: "
        s += str(self.field_modified)
        s += "\n"
        s += "Last modified by "
        s += str(self.origin)
        s += " on: "
        s += self.lastupdate
        s += "\n"
        s += "Value according to "
        s += str(self.origin)
        s += ": "
        s += "\x1b[2;30;42m" + str(self.value_in_origin_catalogue) + "\x1b[0m"
        s += "\n"
        s += "Value according to Open Exoplanet Catalogue: "
        s += "\x1b[6;30;41m" + str(self.value_in_OEC) + "\x1b[0m"
        s += "\n"
        s += "Origin Upper Limit: "
        s += "\x1b[2;30;42m" + str(self.origin_upper) + "\x1b[0m"
        s += "\n"
        s += "Origin Lower Limit: "
        s += "\x1b[2;30;42m" + str(self.origin_lower) + "\x1b[0m"
        s += "\n"
        s += "OEC Upper Limit: "
        s += "\x1b[6;30;41m" + str(self.OEC_upper) + "\x1b[0m"
        s += "\n"
        s += "OEC Lower Limit: "
        s += "\x1b[6;30;41m" + str(self.OEC_lower) + "\x1b[0m"
        s += "\n"

        return s

    def get_object_name(self):
        '''
        () -> str
        Returns the name of the PlanetaryObject to which this instance of 
        proposed addition is referring.
        '''
        if self.OEC_object is not None:
            return self.OEC_object.name
        else:
            return ""

    def getSystemName(self):
        ''' () -> str
        Return the system name that the oec object is in
        '''
        if self.OEC_object.__class__.__name__ != "System":
            if self.OEC_object.__class__.__name__ == "Star":
                sysName = self.OEC_object.nameSystem
            elif self.OEC_object.__class__.__name__ == "Planet":
                sysName = self.OEC_object.starObject.nameSystem
        else:
            sysName = self.OEC_object.name
        return sysName

    def getOECType(self):
        ''' () -> str
        Return the type of object that the oec object is
        '''
        return self.OEC_object.__class__.__name__


def merge_changes(first, second):
    '''
    ([ProposedChange], [ProposedChange]) -> [ProposedChange]
    
    Helper method for merge_sort_changes() method. Merges 2 sorted lists of
    proposed changes; returns single sorted list.
    '''
    # List res will contain all the elements from both lists
    res = []
    # Append ProposedChange objects by lexicographical order of the name of the
    # planetaryObject ProposedChanges are referring to
    while len(first) != 0 and len(second) != 0:
        if first[0].get_object_name() < second[0].get_object_name():
            res.append(first.pop(0))
        else:
            res.append(second.pop(0))
    # Add all the elements from the list that is not empty to the res
    for i in [first, second]:
        res.extend(i)
    return res


def merge_sort_changes(CHANGES):
    '''
    ([ProposedChange]) -> [ProposedChange]
    
    Recursively sorts the list of proposed changes in lexicographical order by
    the name of the object the change is referring to. Returns sorted list.
    '''
    if len(CHANGES) > 1:
        mid = len(CHANGES) // 2
        # Recursive calls on first and second halves.
        first = merge_sort_changes(CHANGES[:mid])
        second = merge_sort_changes(CHANGES[mid:])
        # Merging and returning 2 sublists
        return merge_changes(first, second)
    else:
        return CHANGES


def bubble_sort_changes_by_lastupdate(CHANGES):
    """ ([ProposedChanged]) -> ([ProposedChange], [int])
    """
    newChanges = CHANGES[:]
    indeces = list(range(len(newChanges)))
    for i in range(len(newChanges)):
        for k in range(len(newChanges) - 1, i, -1):
            if (dt.strptime(newChanges[k].lastupdate, "%y/%m/%d") > dt.strptime(
                    newChanges[k - 1].lastupdate, "%y/%m/%d")):
                (newChanges[k], newChanges[k - 1]) = (
                    newChanges[k - 1], newChanges[k])
                (indeces[k], indeces[k - 1]) = (indeces[k - 1], indeces[k])
    return (newChanges, indeces)


def merge_changes_by_last_update(first, second):
    '''
    ([ProposedChange], [ProposedChange]) -> [ProposedChange]

    Helper method for merge_sort_changes() method. Merges 2 sorted lists of
    proposed changes; returns single sorted list.
    '''
    # List res will contain all the elements from both lists
    res = []
    # Append ProposedChange objects by lexicographical order of the name of the
    # planetaryObject ProposedChanges are referring to
    while len(first) != 0 and len(second) != 0:
        if (dt.strptime(first[0].lastupdate, "%y/%m/%d") > dt.strptime(
                second[0].lastupdate, "%y/%m/%d")):
            res.append(first.pop(0))
        else:
            res.append(second.pop(0))
    # Add all the elements from the list that is not empty to the res
    for i in [first, second]:
        res.extend(i)
    return res


def merge_sort_changes_by_lastupdate(CHANGES):
    '''
    ([ProposedChange]) -> [ProposedChange]

    Recursively sorts the list of proposed changes in lexicographical order by
    the name of the object the change is referring to. Returns sorted list.
    '''
    if len(CHANGES) > 1:
        mid = len(CHANGES) // 2
        # Recursive calls on first and second halves.
        first = merge_sort_changes_by_lastupdate(CHANGES[:mid])
        second = merge_sort_changes_by_lastupdate(CHANGES[mid:])
        # Merging and returning 2 sublists
        return merge_changes_by_last_update(first, second)
    else:
        return CHANGES


def sort_changes_lastupdate(changes_list):
    """([ProposedChange]) -> [ProposedChange]
    Given a list of proposde changes, sort it by the lastupdate field and
    return it
    """
    newChangesList = changes_list[:]
    for i in range(len(changes_list)):
        newChangesList[i]._index = i
    newChangesList = merge_sort_changes_by_lastupdate(newChangesList)
    return newChangesList


def sort_changes(changes_list):
    '''
    ([ProposedChange]) -> None
    
    In place sorting for the list of proposed changes. Relies on 
    merge_sort_changes.
    '''
    changes_list = merge_sort_changes(changes_list)
