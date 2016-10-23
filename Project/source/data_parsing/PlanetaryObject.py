class PlanetaryObject:
    def __init__(self, name=None):
        if name is None:
            self.data = dict()
        else:
            self.data = {"name" + self.__class__.__name__, name}

    def __str__(self):
        '''
        Builds up and returns a human-readable representation of 
        PlanetaryObject, including all the keys and corresponding data values;
        If references to other planetary objects are present, they are ignored.
        '''
        list_objects = ["Planet", "Star", "System", "PlanetaryObject"]
        s = ""
        s += "Object type : "
        s += self.__class__.__name__
        s += "\n"
        for key in self.data.keys():
            s += str(key)
            s += " :   "
            if self.data[key].__class__.__name__ in list_objects :
                s += "Points to an instance of class "
                s += self.data[key].__class__.__name__
            else:
                s += str(self.data[key])
            s += "\n"
        s += "\n"
        return s

    def addVal(self, name, val):
        if isinstance(val, PlanetaryObject):
            self.data[name] = val
        else:
            val = self._fixVal(val)
            self.data[name] = val

    def addValList(self, name, val):
        if isinstance(val, list):
            self.data[name] = val
        else:
            val = self._fixVal(val)
            self.data[name] = [val]
        return self

    def addToValList(self, name, val):
        val = self._fixVal(val)
        self.data[name] += [val]
        return self

    def getData(self):
        return self.data

    def getVal(self, name):
        return self.data[name]

    def _fixVal(self, val):
        temp = None
        if (val != ''):
            try:
                temp = float(val)
            except ValueError:
                temp = val
            except TypeError:
                temp = "N/A"
        else:
            temp = "N/A"
        return temp
