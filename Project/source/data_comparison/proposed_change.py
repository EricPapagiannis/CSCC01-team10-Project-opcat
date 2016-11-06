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
        ProposedChange.__init__(self, origin)

    def __str__(self):
        s = "Proposed addition:\n"
        s += "From : "
        s += str(self.origin)
        s += "\n"
        s += "Type of object: "
        s += self.object_ptr.__class__.__name__
        s += "\n"
        s += "Stats:\n"
        s += str(self.object_ptr)
        s += "\n"
        return s


    def get_object_name():
        '''
        () -> str
        
        Returns the name of the PlanetaryObject to which this instance of 
        proposed addition is referring.
        '''
        if self.object_ptr is not None :
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

    def __init__(self, origin, OEC_object,
                 field_modified, value_in_origin_catalogue, value_in_OEC):
        self.OEC_object = OEC_object
        self.field_modified = field_modified
        self.value_in_origin_catalogue = value_in_origin_catalogue
        self.value_in_OEC = value_in_OEC
        ProposedChange.__init__(self, origin)

    def __str__(self):
        s = "Proposed modification:\n"
        s += "Origin : "
        s += str(self.origin)
        s += "\n"
        s += "Type of object modified: "
        s += str(self.OEC_object.__class__.__name__)
        s += "\n"
        s += "Name of object modified: "
        s += self.OEC_object.name
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
        s += "\nValue according to "
        s += str(self.origin)
        s += ": "
        s += str(self.value_in_origin_catalogue)
        s += "\n"
        s += "Value according to Open Exoplanet Catalogue: "
        s += str(self.value_in_OEC)
        s += "\n"
        return s
    
    def get_object_name():
        '''
        () -> str
        
        Returns the name of the PlanetaryObject to which this instance of 
        proposed addition is referring.
        '''        
        if self.OEC_object is not None :
            return self.OEC_object.name
        else:
            return ""    


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
    while len(first) != 0 and len(second) != 0 :
        if first[0].get_object_name() > second[0].get_object_name() :
            res.append(first.pop(0))
        else:
            res.append(second.pop(0))
    # Add all the elements from the list that is not empty to the res
    for i in [first, second] :
        res.extend(i)
    return res
    

def merge_sort_changes(CHANGES):
    '''
    ([ProposedChange]) -> [ProposedChange]
    
    Recursively sorts the list of proposed changes in lexicographical order by
    the name of the object the change is referring to. Returns sorted list.
    '''
    mid = len(CHANGES) // 2
    # Recursive calls on first and second halves.
    first = merge_sort_changes(CHANGES[:mid])
    second = merge_sort_changes(CHANGES[mid:])
    # Merging and returning 2 sublists
    return merge_changes(first, second)


if __name__ == "__main__":
    p = []
    q = {}
    a = Addition("exoplanet.eu", p)
    print(a)

    m = Modification("NASA archive", p, q, "mass", 100, 200)
    print(m)
