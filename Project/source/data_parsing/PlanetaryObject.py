class PlanetaryObject:
    def __init__(self, name=None):
        if isinstance(name, str):
            self.data[name] = self._fixStr(name)
        self.name = self._fixStr(name)
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
        if isinstance(name, str):
            name = self._fixStr(name)

        if isinstance(val, PlanetaryObject):
            self.data[name] = val
        elif isinstance(val, str):
            self.data[name] = self._fixStr(val)
        else:
            val = self._fixVal(val)
            self.data[name] = val

    def addValList(self, name, val):
        if isinstance(name, str):
            name = self._fixStr(name)

        if isinstance(val, list):
            self.data[name] = val
        elif isinstance(val, str):
            self.data[name] = [self._fixStr(val)]
        else:
            val = self._fixVal(val)
            self.data[name] = [val]
        return self

    def addToValList(self, name, val):
        if isinstance(name, str):
            name = self._fixStr(name)
        if isinstance(val, str):
            val = self._fixStr(val)
        else:
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

    def _fixStr(self, val):
        if isinstance(val, str):
            return val.replace("\"", "").strip()
        else:
            return val

if __name__ == "__main__":
    print("\"CH4".replace("\"", "").strip())