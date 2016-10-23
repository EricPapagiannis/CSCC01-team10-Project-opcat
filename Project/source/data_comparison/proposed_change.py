class ProposedChange:
    '''
    Abstract class. Not used directly. Parent Class of Addition and 
    Modicfication
    '''
    def __init__(self, origin):
        if origin == "NASA":
            self.origin = "NASA"
        else:
            self.origin = "exoplanet.eu"

class Addition(ProposedChange):
    
    '''
    object_ptr is the pointer to PlanetaryObject instance to be added.
    '''
    def __init__(self, origin, object_ptr):
        self.object_ptr = object_ptr
        ProposedChange.__init__(self, origin)
        
        
class Modification(ProposedChange):
    
    '''
    target_system_ptr is the pointer to PlanetaryObject instance originating 
    from one of target catalogues (NASA, exoplanet.eu). OEC_system_ptr is the 
    pointer to planetary object originating from Open Exoplanet Catalogue.
    
    target_system_ptr and OEC_system_ptr must be of the same subclass; ex: both
    Star objects or both Planet objects
    '''
    def __init__(self, origin, target_system_ptr, OEC_system_ptr):
        self.target_system_ptr = target_system_ptr
        self.OEC_system_ptr = OEC_system_ptr
        ProposedChange.__init__(self, origin)
