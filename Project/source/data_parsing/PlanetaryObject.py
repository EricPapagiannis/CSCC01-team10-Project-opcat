class PlanetaryObject:
    def __init__(self, name=None):
        if name is None:
            self.data = dict()
        else:
            self.data = {"name" + self.__class__.__name__, name}

    def __str__(self):
        return str(self.data)

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
